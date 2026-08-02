"""하차 정류장 선정 유스케이스를 조율하고 최적 후보를 결정한다."""

from app.clients.tmap import TMapClient
from app.repositories.stop_repository import CsvStopRepository
from app.schemas.destination import DestinationCandidate
from app.schemas.location import Coordinate
from app.schemas.stop import DropoffStopSelectionResponse
from app.services.stop.walking_selection import (
    StopWalkingDirection,
    select_optimal_stop,
)


async def find_optimal_dropoff_stop(
    destination: DestinationCandidate,
    repository: CsvStopRepository | None = None,
    client: TMapClient | None = None,
) -> DropoffStopSelectionResponse:
    stop_repository = repository or CsvStopRepository()
    stops = stop_repository.get_all()

    result = await select_optimal_stop(
        reference=Coordinate(
            latitude=destination.latitude,
            longitude=destination.longitude,
        ),
        reference_name=destination.name,
        stops=stops,
        direction=StopWalkingDirection.FROM_STOP,
        client=client,
    )

    return DropoffStopSelectionResponse(
        destination=destination,
        selected_stop=result.selected_stop,
        evaluated_stops=result.evaluated_stops,
        message=(
            f"{result.selected_stop.stop.name} 정류장이 목적지까지의 "
            "보행시간이 가장 짧습니다."
        ),
    )
