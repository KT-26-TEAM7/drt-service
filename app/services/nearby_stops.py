from math import atan2, cos, radians, sin, sqrt

from app.config import NEARBY_STOP_CANDIDATE_COUNT
from app.repositories.stop_repository import CsvStopRepository
from app.schemas.stop import DRTStop, NearbyStopCandidate

EARTH_RADIUS_METERS = 6_371_000


def _calculate_straight_distance(
    start_latitude: float,
    start_longitude: float,
    end_latitude: float,
    end_longitude: float,
) -> float:
    start_latitude_rad = radians(start_latitude)
    end_latitude_rad = radians(end_latitude)

    latitude_difference = radians(end_latitude - start_latitude)
    longitude_difference = radians(end_longitude - start_longitude)

    haversine_value = (
        sin(latitude_difference / 2) ** 2
        + cos(start_latitude_rad)
        * cos(end_latitude_rad)
        * sin(longitude_difference / 2) ** 2
    )

    central_angle = 2 * atan2(
        sqrt(haversine_value),
        sqrt(1 - haversine_value),
    )

    return EARTH_RADIUS_METERS * central_angle


def find_nearby_stops(
    destination_latitude: float,
    destination_longitude: float,
    stops: list[DRTStop],
    limit: int = NEARBY_STOP_CANDIDATE_COUNT,
) -> list[NearbyStopCandidate]:
    candidates = []

    for stop in stops:
        distance = _calculate_straight_distance(
            start_latitude=destination_latitude,
            start_longitude=destination_longitude,
            end_latitude=stop.latitude,
            end_longitude=stop.longitude,
        )

        candidates.append(
            NearbyStopCandidate(
                stop=stop,
                straight_distance_m=round(distance, 1),
            )
        )

    candidates.sort(key=lambda candidate: candidate.straight_distance_m)

    return candidates[:limit]


def find_nearby_stops_from_csv(
    destination_latitude: float,
    destination_longitude: float,
    repository: CsvStopRepository | None = None,
) -> list[NearbyStopCandidate]:
    stop_repository = repository or CsvStopRepository()
    stops = stop_repository.get_all()

    return find_nearby_stops(
        destination_latitude=destination_latitude,
        destination_longitude=destination_longitude,
        stops=stops,
    )
