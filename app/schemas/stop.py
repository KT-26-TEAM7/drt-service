from pydantic import BaseModel, ConfigDict, Field


class DRTStop(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    stop_type: str = Field(alias="type")
    ext_id: str | None = None
    latitude: float
    longitude: float


class NearbyStopCandidate(BaseModel):
    stop: DRTStop
    straight_distance_m: float = Field(ge=0)


class StopWalkingRoute(BaseModel):
    stop: DRTStop
    straight_distance_m: float = Field(ge=0)
    walking_distance_m: int = Field(ge=0)
    walking_time_seconds: int = Field(ge=0)