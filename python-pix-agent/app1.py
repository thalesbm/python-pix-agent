from pydantic import BaseModel
from typing import Optional
from langgraph.types import interrupt
from langgraph.graph import StateGraph, END

class GraphState(BaseModel):
    user_message: str
    valor: Optional[float] = None

def verificar_valor(state: GraphState) -> GraphState:
    print("🚀 Entrou no nó verificar_valor")
    
    if state.valor is None:
        print("⚠️ Valor está ausente, lançando interrupt")
        raise interrupt({
            "message": "Qual valor você deseja definir?"
        })

    print("✅ Valor recebido:", state.valor)
    return state

graph_builder = StateGraph(GraphState)
graph_builder.add_node("verificar_valor", verificar_valor)

graph_builder.set_entry_point("verificar_valor")

compiled_graph = graph_builder.compile()

state = GraphState(user_message="Quero atualizar o limite")

steps = compiled_graph.stream(state)

print(type(steps))
print(steps)

for step in steps:
    print("📦 step:", step)
    if "__interrupt__" in step:
        intr = step["__interrupt__"][0]
        print("🚫 Interrompido com:", intr.value["message"])