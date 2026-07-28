from typing import Any
from urllib.parse import quote

from app.clients.tmap import TMapClient
from app.schemas.destination import DestinationCandidate
from app.schemas.stop import NearbyStopCandidate, StopWalkingRoute


class WalkingRouteError(RuntimeError):
    """TMAP 보행자 경로 응답 처리 중 발생한 오류."""


def _extract_walking_summary(data: dict[str, Any]) -> tuple[int, int]:
    features = data.get("features")

    if not isinstance(features, list):
        raise WalkingRouteError("TMAP 보행자 경로 응답의 features 형식이 올바르지 않습니다.")

    for feature in features:
        if not isinstance(feature, dict):
            continue

        properties = feature.get("properties")

        if not isinstance(properties, dict):
            continue

        if properties.get("pointType") != "SP":
            continue

        total_distance = properties.get("totalDistance")
        total_time = properties.get("totalTime")

        try:
            return int(total_distance), int(total_time)
        except (TypeError, ValueError) as error:
            raise WalkingRouteError("TMAP 보행자 경로의 거리 또는 시간 값이 올바르지 않습니다.") from error

    raise WalkingRouteError("TMAP 보행자 경로 응답에서 전체 거리와 시간을 찾을 수 없습니다.")


async def calculate_walking_route(
    candidate: NearbyStopCandidate,
    destination: DestinationCandidate,
    client: TMapClient | None = None,
) -> StopWalkingRoute:
    tmap_client = client or TMapClient()
    stop = candidate.stop

    request_body = {
        "startX": stop.longitude,
        "startY": stop.latitude,
        "endX": destination.longitude,
        "endY": destination.latitude,
        "startName": quote(stop.name),
        "endName": quote(destination.name),
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "searchOption": "0",
        "sort": "index",
    }

    data = await tmap_client.post(
        path="/routes/pedestrian",
        params={"version": "1"},
        json=request_body,
    )

    walking_distance, walking_time = (_extract_walking_summary(data))

    return StopWalkingRoute(
        stop=stop,
        straight_distance_m=candidate.straight_distance_m,
        walking_distance_m=walking_distance,
        walking_time_seconds=walking_time,
    )