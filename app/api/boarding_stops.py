from fastapi import APIRouter, HTTPException, status

from app.clients.tmap import TMapAPIError
from app.repositories.stop_repository import StopRepositoryError
from app.schemas.stop import (
    BoardingStopSelectionRequest,
    BoardingStopSelectionResponse,
)
from app.services.stop.boarding import find_optimal_boarding_stop
from app.services.stop.walking_selection import StopSelectionError

router = APIRouter(
    prefix="/api/boarding-stops",
    tags=["boarding-stops"],
)


@router.post(
    "/select",
    response_model=BoardingStopSelectionResponse,
    summary="최적 승차 정류장 선택",
)
async def select_boarding_stop_api(
    request: BoardingStopSelectionRequest,
) -> BoardingStopSelectionResponse:
    try:
        return await find_optimal_boarding_stop(current_location=request)
    except StopRepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error
    except (TMapAPIError, StopSelectionError) as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
