from fastapi import APIRouter, HTTPException, status

from app.repositories.stop_repository import StopRepositoryError
from app.schemas.stop import DropoffStopSelectionRequest, DropoffStopSelectionResponse
from app.services.select_dropoff_stop import DropoffStopSelectionError, find_optimal_dropoff_stop
from app.services.route_walking import WalkingRouteError


router = APIRouter(
    prefix="/api/dropoff-stops",
    tags=["dropoff-stops"],
)


@router.post(
    "/select",
    response_model=DropoffStopSelectionResponse,
)
async def select_dropoff_stop_api(request: DropoffStopSelectionRequest) -> DropoffStopSelectionResponse:
    try:
        return await find_optimal_dropoff_stop(
            destination=request.destination,
        )

    except StopRepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

    except WalkingRouteError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    except DropoffStopSelectionError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error