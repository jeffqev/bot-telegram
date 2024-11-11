from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.expenses.cases.analyze_expense import (
    AnalyzeExpenseCase,
    AnalyzeExpenseRequest,
    AnalyzeExpenseResponse,
)
from app.dependencies_factory.cases import analyze_expense_use_case
from app.config.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.expenses.domain.exceptions import (
    UserNotFoundException,
    NoExpensesFoundException,
    FieldValidation,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request, exc):
    return JSONResponse(status_code=401, content={"message": str(exc)})


@app.exception_handler(NoExpensesFoundException)
async def no_expenses_found_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(FieldValidation)
async def no_expenses_found_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": str(exc)})


@app.get("/health_check")
def health_check():
    return {"status": "ok"}


@app.post("/analyze_expense", response_model=AnalyzeExpenseResponse)
async def analyze_expense(
    request: AnalyzeExpenseRequest,
    session: AsyncSession = Depends(get_db_session),
):
    use_case: AnalyzeExpenseCase = await analyze_expense_use_case(session=session)
    return await use_case(request=request)
