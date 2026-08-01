from enum import Enum

from pydantic import BaseModel, Field


class DestinationCandidate(BaseModel):
    tmap_id: str
    name: str
    phone: str | None = None

    latitude: float
    longitude: float

    address: str | None = None
    district: str | None = None
    neighborhood: str | None = None

    category: str | None = None
    detail_category: str | None = None


class DestinationSearchType(str, Enum):
    NOT_FOUND = "not_found"
    SINGLE = "single"
    MULTIPLE = "multiple"


class DestinationSearchResponse(BaseModel):
    total_count: int = Field(ge=0)
    search_type: DestinationSearchType
    message: str
    destinations: list[DestinationCandidate]