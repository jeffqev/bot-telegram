import pydantic

class AddUserResponse(pydantic.BaseModel):
    id: int
    external_id: str