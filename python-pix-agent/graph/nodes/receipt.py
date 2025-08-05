from model.graph_state import GraphState

def receipt(state: GraphState) -> GraphState:
    state.receipt = "O Comprovante foi gerado com sucesso!"
    return state
