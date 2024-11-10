from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.expenses.cases.analyze_expense import (
    AnalyzeExpenseRequest,
    AnalyzeExpenseResponse,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health_check")
def health_check():
    return {"status": "ok"}


@app.post("/analyze_expense", response_model=AnalyzeExpenseResponse)
def analyze_expense(request: AnalyzeExpenseRequest):
    return AnalyzeExpenseResponse(
        response=[
            AnalyzeExpenseResponse.Expense(
                description="test", amount=10, category="test"
            )
        ]
    )
