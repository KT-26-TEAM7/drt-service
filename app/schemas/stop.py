from pydantic import BaseModel, Field

from app.schemas.destination import DestinationCandidate


class DRTStop(BaseModel):
    id: int
    name: str
    stop_type: str
    ext_id: str | None = None
    latitude: float
    longitude: float


class DropoffStopCandidate(BaseModel):
    stop: DRTStop
    straight_distance_m: float = Field(ge=0)


class StopWalkingRoute(BaseModel):
    stop: DRTStop
    straight_distance_m: float = Field(ge=0)
    walking_distance_m: int = Field(ge=0)
    walking_time_seconds: int = Field(ge=0)


class DropoffStopSelectionRequest(BaseModel):
    destination: DestinationCandidate


class DropoffStopSelectionResponse(BaseModel):
    destination: DestinationCandidate
    selected_stop: StopWalkingRoute
    evaluated_stops: list[StopWalkingRoute]
    message: str
