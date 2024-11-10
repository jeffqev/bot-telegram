import pydantic


class User(pydantic.BaseModel):
    id: int
    external_id: str
