"""좌표 사이의 지리적 거리를 계산한다."""

from math import atan2, cos, radians, sin, sqrt

EARTH_RADIUS_METERS = 6_371_000


def calculate_haversine_distance_m(
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
    haversine_value = min(1.0, max(0.0, haversine_value))

    central_angle = 2 * atan2(
        sqrt(haversine_value),
        sqrt(1 - haversine_value),
    )

    return EARTH_RADIUS_METERS * central_angle
