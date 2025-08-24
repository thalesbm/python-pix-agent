from infra.openai_client import OpenAIClientFactory

_llm = None

def get_client_instance():
    global _llm
    if _llm is None:
        _llm = OpenAIClientFactory().create_basic_client()
    return _llm
