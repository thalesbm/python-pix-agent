from model.graph_state import GraphState

def input_message(state: GraphState) -> GraphState:
    print(">> Entrou no nó de input_message")
    state.user_message = input("O que você deseja fazer?").strip().lower()
    return state
