import pydantic
from pydantic import field_validator
from app.expenses.domain.exceptions import FieldValidation


class AnalyzeExpenseRequest(pydantic.BaseModel):
    user_id: str
    text: str

    @field_validator('text')
    def text_must_not_be_empty_or_spaces(cls, v):
        if not v.strip():
            raise FieldValidation('text must not be empty or contain only spaces')
        return v
