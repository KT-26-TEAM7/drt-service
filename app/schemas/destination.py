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


class DestinationSearchResponse(BaseModel):
    total_count: int = Field(ge=0)
    destinations: list[DestinationCandidate]