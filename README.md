# Expenses AI Telegram Bot

This project is a Telegram bot that facilitates the addition of expenses to a database using AI. For example, you can send a message like "Pizza 20 dollars" and the bot will handle the rest.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/jeffqev/expenses-ai-telegram-bot.git
    cd expenses-ai-telegram-bot
    ```

2. Replace .env.example in bot-telegram and ai-services with your api keys

    Telegram Api key: https://core.telegram.org/api/obtaining_api_id
    
    Open ai Api key: https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key



2. Build and start the services:

    ```sh
    make up
    ```

3. Check the logs to ensure the services are running correctly:

    ```sh
    make logs
    ```

4. Run tests to ensure everything is working:

    ```sh
    make test
    ```

> Note: Don't forget to add your telegram id in the database

## Makefile Commands

The Makefile provides several commands to help with development, testing, and deployment of the project. Below is a list of the available commands and their descriptions:

### `up`

Starts the services defined in the Docker Compose file.

```sh
make up
```

### `logs`

Displays the logs for the ai-api and bot services.

```sh
make logs
```

### `test`

Runs the tests for both the bot and ai-api services.

```sh
make test
```
> Note: if you need to run the test separately run `make-bot` or `make test-ai` 

### `clean`

Stops and removes all containers, networks, volumes, and images created by Docker Compose.

```sh
make clean
```

### `shell-bot`

Opens a shell in the bot service container.

```sh
make shell-bot
```

### `shell-ai`

Opens a shell in the ai api service container.

```sh
make shell-ai
```