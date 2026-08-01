from app.clients.tmap import TMapClient
from app.repositories.stop_repository import CsvStopRepository
from app.schemas.destination import DestinationCandidate
from app.schemas.stop import StopWalkingRoute, DropoffStopSelectionResponse
from app.services.nearby_stops import find_nearby_stops
from app.services.route_walking import calculate_walking_routes


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

    nearby_candidates = find_nearby_stops(
        destination_latitude=destination.latitude,
        destination_longitude=destination.longitude,
        stops=stops,
    )

    walking_routes = await calculate_walking_routes(
        candidates=nearby_candidates,
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
            f"{selected_stop.stop.name} 정류장이 "
            "목적지까지의 보행시간이 가장 짧습니다."
        ),
    )