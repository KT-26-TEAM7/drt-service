"""현재 위치에서 보행 접근시간이 가장 짧은 승차 정류장을 선정한다."""

from app.clients.tmap import TMapClient
from app.repositories.stop_repository import CsvStopRepository
from app.schemas.location import Coordinate
from app.schemas.stop import BoardingStopSelectionResponse
from app.services.stop.walking_selection import (
    StopWalkingDirection,
    select_optimal_stop,
)


async def find_optimal_boarding_stop(
    current_location: Coordinate,
    repository: CsvStopRepository | None = None,
    client: TMapClient | None = None,
) -> BoardingStopSelectionResponse:
    stop_repository = repository or CsvStopRepository()
    result = await select_optimal_stop(
        reference=current_location,
        reference_name="현재 위치",
        stops=stop_repository.get_all(),
        direction=StopWalkingDirection.TO_STOP,
        client=client,
    )
    return BoardingStopSelectionResponse(
        selected_stop=result.selected_stop,
        evaluated_stops=result.evaluated_stops,
        message=(
            f"{result.selected_stop.stop.name} 정류장이 현재 위치에서 "
            "보행시간이 가장 짧습니다."
        ),
    )
