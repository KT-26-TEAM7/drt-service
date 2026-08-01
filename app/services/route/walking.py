"""두 지점 사이의 TMAP 보행경로를 계산한다."""

from typing import Any
from urllib.parse import quote

from app.clients.tmap import TMapClient
from app.schemas.location import Coordinate
from app.schemas.route import WalkingRouteSummary


class WalkingRouteError(RuntimeError):
    """TMAP 보행자 경로 요청 또는 응답 처리 오류."""


def _extract_walking_summary(data: dict[str, Any]) -> tuple[int, int]:
    features = data.get("features")
    if not isinstance(features, list):
        raise WalkingRouteError(
            "TMAP 보행자 경로 응답의 features 형식이 올바르지 않습니다."
        )

    for feature in features:
        if not isinstance(feature, dict):
            continue
        properties = feature.get("properties")
        if not isinstance(properties, dict) or properties.get("pointType") != "SP":
            continue
        try:
            return int(properties["totalDistance"]), int(properties["totalTime"])
        except (KeyError, TypeError, ValueError) as error:
            raise WalkingRouteError(
                "TMAP 보행자 경로의 거리 또는 시간 값이 올바르지 않습니다."
            ) from error

    raise WalkingRouteError(
        "TMAP 보행자 경로 응답에서 전체 거리와 시간을 찾을 수 없습니다."
    )


async def calculate_walking_route(
    start: Coordinate,
    end: Coordinate,
    start_name: str,
    end_name: str,
    client: TMapClient | None = None,
) -> WalkingRouteSummary:
    tmap_client = client or TMapClient()
    data = await tmap_client.post(
        path="/routes/pedestrian",
        params={"version": "1"},
        json={
            "startX": start.longitude,
            "startY": start.latitude,
            "endX": end.longitude,
            "endY": end.latitude,
            "startName": quote(start_name),
            "endName": quote(end_name),
            "reqCoordType": "WGS84GEO",
            "resCoordType": "WGS84GEO",
            "searchOption": "0",
            "sort": "index",
        },
    )
    distance_m, time_seconds = _extract_walking_summary(data)
    return WalkingRouteSummary(
        distance_m=distance_m,
        time_seconds=time_seconds,
    )
