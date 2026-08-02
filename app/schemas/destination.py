from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.location import Coordinate


class DestinationCandidate(Coordinate):
    tmap_id: str
    name: str
    phone: str | None = None

    address: str | None = None
    district: str | None = None
    neighborhood: str | None = None

    category: str | None = None
    detail_category: str | None = None


class DestinationKeywordType(str, Enum):
    EXACT = "exact"
    CATEGORY = "category"


class DestinationSearchType(str, Enum):
    NOT_FOUND = "not_found"
    SINGLE = "single"
    MULTIPLE = "multiple"


class DestinationSearchResponse(BaseModel):
    total_count: int = Field(ge=0)
    search_type: DestinationSearchType
    message: str
    destinations: list[DestinationCandidate]


class DestinationConfirmationStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class DestinationConfirmationRequest(BaseModel):
    confirmed: bool
    destination: DestinationCandidate | None = None


class DestinationConfirmationResponse(BaseModel):
    status: DestinationConfirmationStatus
    message: str
    destination: DestinationCandidate | None = None
