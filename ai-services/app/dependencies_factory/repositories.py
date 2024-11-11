from ..expenses import implementations as repositories
from app.config.langchain import llm_client


def generative_ai_langchain_repository() -> (
    repositories.GenerativeAILangchainRepository
):
    client = llm_client(is_json_response=True)
    return repositories.GenerativeAILangchainRepository(llm_client=client)


def user_repository(session) -> repositories.UserPostgresRepository:
    return repositories.UserPostgresRepository(session=session)


def expenses_repository(session) -> repositories.ExpensesPostgresRepository:
    return repositories.ExpensesPostgresRepository(
        session=session,
        generative_ai_repository=generative_ai_langchain_repository(),
    )
