import abc
import typing
from ..entities import Expense, ExpenseCreation, AnalyzedExpense


class ExpensesRepository(abc.ABC):
    @abc.abstractmethod
    async def bulk_insert(
        self,
        expenses: typing.List[ExpenseCreation],
    ) -> typing.List[Expense]:
        """
        Bulk insert expenses

        Args:
            expenses (List[ExpenseCreation]): The expenses to insert

        Returns:
            List[Expense]: The inserted expenses

        """
        pass

    async def analyze_from_text(self, text: str) -> typing.List[AnalyzedExpense]:
        """
        Analyze expenses

        Args:
            text (str): The text to analyze

        Returns:
            List[AnalyzedExpense]: The analyzed expenses

        """
        pass
