from pydantic import BaseModel, Field

from app.schemas.destination import DestinationCandidate
from app.schemas.stop import StopWalkingRoute


class WalkingRouteSummary(BaseModel):
    distance_m: int = Field(ge=0)
    time_seconds: int = Field(ge=0)


class DrtRouteSummary(BaseModel):
    distance_m: int = Field(ge=0)
    time_seconds: int = Field(ge=0)


class DestinationRouteEvaluation(BaseModel):
    destination: DestinationCandidate
    boarding_stop: StopWalkingRoute
    dropoff_stop: StopWalkingRoute
    drt_route: DrtRouteSummary
    total_distance_m: int = Field(ge=0)
    total_time_seconds: int = Field(ge=0)


class CategoryDestinationSelectionResponse(BaseModel):
    selected: DestinationRouteEvaluation
    evaluated_destinations: list[DestinationRouteEvaluation]
    message: str
