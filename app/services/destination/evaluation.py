"""목적지별 보행·DRT 구간의 전체 이동 비용을 합산한다."""

from app.schemas.destination import DestinationCandidate
from app.schemas.route import DestinationRouteEvaluation, DrtRouteSummary
from app.schemas.stop import StopWalkingRoute


def evaluate_destination_route(
    *,
    destination: DestinationCandidate,
    boarding_stop: StopWalkingRoute,
    dropoff_stop: StopWalkingRoute,
    drt_route: DrtRouteSummary,
) -> DestinationRouteEvaluation:
    return DestinationRouteEvaluation(
        destination=destination,
        boarding_stop=boarding_stop,
        dropoff_stop=dropoff_stop,
        drt_route=drt_route,
        total_distance_m=(
            boarding_stop.walking_distance_m
            + drt_route.distance_m
            + dropoff_stop.walking_distance_m
        ),
        total_time_seconds=(
            boarding_stop.walking_time_seconds
            + drt_route.time_seconds
            + dropoff_stop.walking_time_seconds
        ),
    )
