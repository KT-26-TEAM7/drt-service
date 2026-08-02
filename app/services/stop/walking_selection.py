"""기준 위치와 보행시간이 가장 짧은 정류장을 공통 방식으로 선정한다."""

from enum import Enum
from math import ceil

from app.clients.tmap import TMapAPIError, TMapClient
from app.config import (
    NEARBY_STOP_FALLBACK_DISTANCE_M,
    WALKING_SPEED_M_PER_SECOND,
)
from app.schemas.location import Coordinate
from app.schemas.stop import DRTStop, StopSelectionResult, StopWalkingRoute
from app.services.route.walking import WalkingRouteError, calculate_walking_route
from app.services.stop.proximity import find_nearest_stops


class StopWalkingDirection(str, Enum):
    TO_STOP = "to_stop"
    FROM_STOP = "from_stop"


class StopSelectionError(RuntimeError):
    """보행경로를 기준으로 정류장을 선택할 수 없는 경우의 오류."""


async def select_optimal_stop(
    *,
    reference: Coordinate,
    reference_name: str,
    stops: list[DRTStop],
    direction: StopWalkingDirection,
    client: TMapClient | None = None,
) -> StopSelectionResult:
    candidates = find_nearest_stops(
        reference=reference,
        stops=stops,
    )
    if not candidates:
        raise StopSelectionError("선택할 수 있는 정류장 후보가 없습니다.")

    tmap_client = client or TMapClient()
    walking_routes: list[StopWalkingRoute] = []
    last_error: TMapAPIError | WalkingRouteError | None = None

    for candidate in candidates:
        stop = candidate.stop
        stop_coordinate = Coordinate(
            latitude=stop.latitude,
            longitude=stop.longitude,
        )
        if direction is StopWalkingDirection.TO_STOP:
            start, end = reference, stop_coordinate
            start_name, end_name = reference_name, stop.name
        else:
            start, end = stop_coordinate, reference
            start_name, end_name = stop.name, reference_name

        try:
            walking_route = await calculate_walking_route(
                start=start,
                end=end,
                start_name=start_name,
                end_name=end_name,
                client=tmap_client,
            )
        except (TMapAPIError, WalkingRouteError) as error:
            last_error = error
            # 출발지와 도착지가 너무 가까우면 TMAP 보행경로 요청이 실패할 수 있으므로
            # 직선거리 기반 대체 경로를 사용해 해당 정류장이 평가에서 누락되지 않게 한다.
            if candidate.straight_distance_m <= NEARBY_STOP_FALLBACK_DISTANCE_M:
                fallback_distance_m = ceil(candidate.straight_distance_m)
                walking_routes.append(
                    StopWalkingRoute(
                        stop=stop,
                        straight_distance_m=candidate.straight_distance_m,
                        walking_distance_m=fallback_distance_m,
                        walking_time_seconds=ceil(
                            fallback_distance_m / WALKING_SPEED_M_PER_SECOND
                        ),
                    )
                )
            continue

        walking_routes.append(
            StopWalkingRoute(
                stop=stop,
                straight_distance_m=candidate.straight_distance_m,
                walking_distance_m=walking_route.distance_m,
                walking_time_seconds=walking_route.time_seconds,
            )
        )

    if not walking_routes:
        raise StopSelectionError(
            "모든 정류장 후보의 보행경로 계산에 실패했습니다."
        ) from last_error

    selected = min(
        walking_routes,
        key=lambda route: (
            route.walking_time_seconds,
            route.walking_distance_m,
            route.straight_distance_m,
            route.stop.id,
        ),
    )
    return StopSelectionResult(
        selected_stop=selected,
        evaluated_stops=walking_routes,
    )
