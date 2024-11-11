from langchain_openai import ChatOpenAI

def llm_client(is_json_response: bool = False) -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o-mini",
        model_kwargs={"response_format": {"type": "json_object"}} if is_json_response else {},
    )
