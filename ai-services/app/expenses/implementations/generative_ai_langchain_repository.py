from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.expenses.domain.repositories import GenerativeAIRepository

class GenerativeAILangchainRepository(GenerativeAIRepository):
    def __init__(self, llm_client: ChatOpenAI):
        self.llm_client = llm_client

    async def ask(self, prompt: str, template: str) -> str:
        try:
            prompt_template = ChatPromptTemplate.from_template(template)
            formatted_prompt = prompt_template.format_messages(user_message=prompt)
            response = await self.llm_client.apredict_messages(formatted_prompt)
            return response.content.strip()
        except Exception as e:
            raise e