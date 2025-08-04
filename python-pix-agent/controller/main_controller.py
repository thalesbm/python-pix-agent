from infra.openai_client import OpenAIClientFactory
from langchain_openai.chat_models import ChatOpenAI
from logger import get_logger
from pipeline.openai import Key
from model.graph_state import GraphState
from langgraph.graph import StateGraph

logger = get_logger(__name__)

class MainController:
    def __init__(self):
        self.api_key = Key.get_openai_key()
        self.openai_client = OpenAIClientFactory(api_key=self.api_key)

    def run(self):
        
        chat: ChatOpenAI = self.openai_client.create_basic_client()

    
        # 5 - Criando o Graph
        graph = StateGraph(GraphState)
        # graph.add_node("responder", responder)
        graph.set_entry_point("responder")
        graph.set_finish_point("responder")

        # 6 - Compilando o Grafo
        export_graph = graph.compile()


        
    # def responder(state):
    #     input_message = state.input
    #     response = llm_model.invoke([HumanMessage(content=input_message)])
    #     return GraphState(
    #         input=state.input, 
    #         output=response.content
    #     )



