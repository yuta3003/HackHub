from pydantic import BaseModel, ConfigDict


class DoneResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
