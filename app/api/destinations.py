from fastapi import APIRouter, HTTPException, Query, status

from app.clients.tmap import TMapAPIError
from app.schemas.destination import (
    DestinationConfirmationRequest,
    DestinationConfirmationResponse,
    DestinationSearchResponse,
)
from app.services.confirm_destination import (
    DestinationConfirmationError,
    confirm_destination,
)
from app.services.search_destinations import (
    DestinationSearchError,
    search_destinations,
)


router = APIRouter(
    prefix="/api/destinations",
    tags=["Destinations"],
)


@router.get(
    "/search",
    response_model=DestinationSearchResponse,
    summary="목적지 후보 검색",
)
async def search_destination_candidates(keyword: str = Query(..., min_length=1, max_length=100)) -> DestinationSearchResponse:
    keyword = keyword.strip()

    if not keyword:
        raise HTTPException(
            status_code=422,
            detail="검색어를 입력해주세요.",
        )

    try:
        return await search_destinations(keyword)
    except (TMapAPIError, DestinationSearchError) as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

@router.post(
    "/confirm",
    response_model=DestinationConfirmationResponse,
    summary="목적지 후보 확인",
)
async def confirm_destination_candidate(request: DestinationConfirmationRequest) -> DestinationConfirmationResponse:
    try:
        return confirm_destination(request)

    except DestinationConfirmationError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error    