"""목적지와 가까운 하차 정류장 후보를 직선거리로 선별한다."""

from app.config import DROPOFF_STOP_CANDIDATE_COUNT
from app.schemas.stop import DropoffStopCandidate, DRTStop
from app.services.geo_distance import calculate_haversine_distance_m


def find_dropoff_stop_candidates(
    destination_latitude: float,
    destination_longitude: float,
    stops: list[DRTStop],
    limit: int = DROPOFF_STOP_CANDIDATE_COUNT,
) -> list[DropoffStopCandidate]:
    candidates = []

    for stop in stops:
        distance = calculate_haversine_distance_m(
            start_latitude=destination_latitude,
            start_longitude=destination_longitude,
            end_latitude=stop.latitude,
            end_longitude=stop.longitude,
        )

        candidates.append(
            DropoffStopCandidate(
                stop=stop,
                straight_distance_m=round(distance, 1),
            )
        )

    candidates.sort(key=lambda candidate: candidate.straight_distance_m)

    return candidates[:limit]
