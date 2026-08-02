from pydantic import BaseModel, Field

from app.schemas.destination import DestinationCandidate
from app.schemas.location import Coordinate


class DRTStop(Coordinate):
    id: int
    name: str
    stop_type: str
    ext_id: str | None = None


class StopCandidate(BaseModel):
    stop: DRTStop
    straight_distance_m: float = Field(ge=0)


class StopWalkingRoute(StopCandidate):
    walking_distance_m: int = Field(ge=0)
    walking_time_seconds: int = Field(ge=0)


class StopSelectionResult(BaseModel):
    selected_stop: StopWalkingRoute
    evaluated_stops: list[StopWalkingRoute]


class DropoffStopSelectionRequest(BaseModel):
    destination: DestinationCandidate


class DropoffStopSelectionResponse(StopSelectionResult):
    destination: DestinationCandidate
    message: str


class BoardingStopSelectionRequest(Coordinate):
    pass


class BoardingStopSelectionResponse(StopSelectionResult):
    message: str
