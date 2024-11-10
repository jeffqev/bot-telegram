import abc


class GenerativeAIRepository(abc.ABC):
    @abc.abstractmethod
    async def ask(self, prompt: str) -> str:
        """
        Ask the generative AI a question

        Args:
            prompt (str): The question to ask

        Returns:
            str: The answer from the generative AI

        """
        pass
