from fastapi import APIRouter, HTTPException, status

from app.clients.tmap import TMapAPIError
from app.repositories.stop_repository import StopRepositoryError
from app.schemas.stop import DropoffStopSelectionRequest, DropoffStopSelectionResponse
from app.services.dropoff_stop_selection import (
    DropoffStopSelectionError,
    find_optimal_dropoff_stop,
)
from app.services.dropoff_walking_routes import WalkingRouteError

router = APIRouter(
    prefix="/api/dropoff-stops",
    tags=["dropoff-stops"],
)


@router.post(
    "/select",
    response_model=DropoffStopSelectionResponse,
)
async def select_dropoff_stop_api(
    request: DropoffStopSelectionRequest,
) -> DropoffStopSelectionResponse:
    try:
        return await find_optimal_dropoff_stop(
            destination=request.destination,
        )

    except StopRepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

    except (TMapAPIError, WalkingRouteError) as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    except DropoffStopSelectionError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error
