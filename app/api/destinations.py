from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.clients.tmap import TMapAPIError
from app.schemas.destination import (
    DestinationConfirmationRequest,
    DestinationConfirmationResponse,
    DestinationKeywordType,
    DestinationSearchResponse,
)
from app.services.destination_confirmation import (
    DestinationConfirmationError,
    confirm_destination,
)
from app.services.destination_search import (
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
async def search_destination_candidates(
    keyword: Annotated[str, Query(min_length=1, max_length=100)],
    departure_latitude: Annotated[float, Query(ge=-90, le=90)],
    departure_longitude: Annotated[float, Query(ge=-180, le=180)],
    keyword_type: Annotated[
        DestinationKeywordType,
        Query(description="exact: 정확한 목적지명, category: 대분류"),
    ] = DestinationKeywordType.EXACT,
) -> DestinationSearchResponse:
    keyword = keyword.strip()

    if not keyword:
        raise HTTPException(
            status_code=422,
            detail="검색어를 입력해주세요.",
        )

    try:
        return await search_destinations(
            keyword=keyword,
            departure_latitude=departure_latitude,
            departure_longitude=departure_longitude,
            keyword_type=keyword_type,
        )
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
async def confirm_destination_candidate(
    request: DestinationConfirmationRequest,
) -> DestinationConfirmationResponse:
    try:
        return confirm_destination(request)

    except DestinationConfirmationError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
