"""하차 정류장 선정 유스케이스를 조율하고 최적 후보를 결정한다."""

from app.clients.tmap import TMapClient
from app.repositories.stop_repository import CsvStopRepository
from app.schemas.destination import DestinationCandidate
from app.schemas.stop import DropoffStopSelectionResponse, StopWalkingRoute
from app.services.dropoff_stop_candidates import find_dropoff_stop_candidates
from app.services.dropoff_walking_routes import calculate_walking_routes


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


async def find_optimal_dropoff_stop(
    destination: DestinationCandidate,
    repository: CsvStopRepository | None = None,
    client: TMapClient | None = None,
) -> DropoffStopSelectionResponse:
    stop_repository = repository or CsvStopRepository()
    stops = stop_repository.get_all()

    dropoff_candidates = find_dropoff_stop_candidates(
        destination_latitude=destination.latitude,
        destination_longitude=destination.longitude,
        stops=stops,
    )

    walking_routes = await calculate_walking_routes(
        candidates=dropoff_candidates,
        destination=destination,
        client=client,
    )

    selected_stop = select_dropoff_stop(
        walking_routes=walking_routes,
    )

    return DropoffStopSelectionResponse(
        destination=destination,
        selected_stop=selected_stop,
        evaluated_stops=walking_routes,
        message=(
            f"{selected_stop.stop.name} 정류장이 목적지까지의 보행시간이 가장 짧습니다."
        ),
    )
