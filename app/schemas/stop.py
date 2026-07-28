from pydantic import BaseModel, ConfigDict, Field


class DRTStop(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    stop_type: str = Field(alias="type")
    ext_id: str | None = None
    latitude: float
    longitude: float