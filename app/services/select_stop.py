from app.schemas.stop import StopWalkingRoute


class DropoffStopSelectionError(RuntimeError):
    """하차 정류장 선택 중 발생한 오류."""


def select_dropoff_stop(walking_routes: list[StopWalkingRoute]) -> StopWalkingRoute:
    if not walking_routes:
        raise DropoffStopSelectionError("선택할 수 있는 정류장 보행경로가 없습니다.")

    return min(
        walking_routes,
        key=lambda route: (
            route.walking_time_seconds,
            route.walking_distance_m,
            route.straight_distance_m,
        ),
    )