import asyncio
import typer

from app.dependencies_factory.cases import add_user_use_case
from app.config.db import create_session_maker
from app.expenses.cases import AddUserRequest

app = typer.Typer()


@app.command()
def add_telegram_user(telegram_id: str):
    sessionmaker = create_session_maker()
    session = sessionmaker()

    request = AddUserRequest(external_id=telegram_id)
    use_case = asyncio.run(add_user_use_case(session))

    user = asyncio.run(use_case(request))

    typer.echo(
        f"User with telegram_id {user.external_id} created with id: {user.id}",
    )
    asyncio.run(session.close())


if __name__ == "__main__":
    app()
