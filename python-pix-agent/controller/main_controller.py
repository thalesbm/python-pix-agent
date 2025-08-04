from infra.openai_client import OpenAIClientFactory
from langchain_openai.chat_models import ChatOpenAI
from logger import get_logger
from pipeline.openai import Key

logger = get_logger(__name__)

class MainController:
    def __init__(self):
        self.api_key = Key.get_openai_key()
        self.openai_client = OpenAIClientFactory(api_key=self.api_key)

    def run(self):
        
        chat: ChatOpenAI = self.openai_client.create_basic_client()

        print(chat.invoke("Olá, como você está?").content)



