import pydantic


class User(pydantic.BaseModel):
    id: int
    external_id: str

class UserCreation(pydantic.BaseModel):
    external_id: str