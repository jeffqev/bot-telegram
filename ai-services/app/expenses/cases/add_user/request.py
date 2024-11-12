import pydantic

class AddUserRequest(pydantic.BaseModel):
    external_id: str