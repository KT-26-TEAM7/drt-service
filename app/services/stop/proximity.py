"""기준 좌표에서 가까운 정류장 후보를 직선거리로 선별한다."""

from app.config import STOP_CANDIDATE_COUNT
from app.schemas.location import Coordinate
from app.schemas.stop import DRTStop, StopCandidate
from app.services.route.geo import calculate_haversine_distance_m


def find_nearest_stops(
    reference: Coordinate,
    stops: list[DRTStop],
    limit: int = STOP_CANDIDATE_COUNT,
) -> list[StopCandidate]:
    candidates = [
        StopCandidate(
            stop=stop,
            straight_distance_m=round(
                calculate_haversine_distance_m(
                    start_latitude=reference.latitude,
                    start_longitude=reference.longitude,
                    end_latitude=stop.latitude,
                    end_longitude=stop.longitude,
                ),
                1,
            ),
        )
        for stop in stops
    ]
    candidates.sort(
        key=lambda candidate: (candidate.straight_distance_m, candidate.stop.id)
    )
    return candidates[:limit]
