from typer.testing import CliRunner

from app.entrypoints.cli import app
from faker import Faker


def test_add_telegram_user_return_the_created_user_when_user_is_a_correct_string(
    cli_runner: CliRunner,
    faker: Faker,
    clear_tables,
):
    fake_telegram_id = str(faker.random_int())
    expected_message = f"User with telegram_id {fake_telegram_id} created"

    result = cli_runner.invoke(app, [fake_telegram_id])

    assert result.exit_code == 0
    assert expected_message in result.stdout
