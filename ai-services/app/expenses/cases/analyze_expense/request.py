import pydantic


class AnalyzeExpenseRequest(pydantic.BaseModel):
    user_id: str
    text: str
