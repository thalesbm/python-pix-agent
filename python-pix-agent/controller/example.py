# from langgraph.graph import StateGraph, END
# from langchain_core.runnables import RunnableLambda
# from langchain_core.messages import HumanMessage
# from langchain_core.runnables.graph import MermaidDrawMethod
# from pydantic import BaseModel
# from typing import TypedDict, Optional


# # 1. Definindo o estado da conversa
# class ConversationState(BaseModel):
#     tipo: Optional[str] = None

# # 2. Nós (funções) do grafo
# def boas_vindas(state: ConversationState) -> ConversationState:
#     print("🤖 Olá! Como posso ajudar você hoje?")
#     return state

# def perguntar_tipo_ajuda(state: ConversationState) -> ConversationState:
#     resposta = input("Você precisa de ajuda com (vendas ou suporte)? ").strip().lower()
#     state.tipo = resposta
#     return state

# def fluxo_vendas(state: ConversationState) -> ConversationState:
#     print("📦 Você escolheu vendas. Temos ótimas promoções!")
#     return state

# def fluxo_suporte(state: ConversationState) -> ConversationState:
#     print("🛠️ Você escolheu suporte. Qual o problema que está enfrentando?")
#     return state

# def finalizar(state: ConversationState) -> ConversationState:
#     print("👋 Obrigado pelo contato. Tenha um ótimo dia!")
#     return state

# # 3. Criando o grafo
# graph_builder = StateGraph(ConversationState)

# # Adiciona nós
# graph_builder.add_node("boas_vindas", RunnableLambda(boas_vindas))
# graph_builder.add_node("pergunta", RunnableLambda(perguntar_tipo_ajuda))
# graph_builder.add_node("vendas", RunnableLambda(fluxo_vendas))
# graph_builder.add_node("suporte", RunnableLambda(fluxo_suporte))
# graph_builder.add_node("finalizar", RunnableLambda(finalizar))

# # Arestas (transições)
# graph_builder.set_entry_point("boas_vindas")
# graph_builder.add_edge("boas_vindas", "pergunta")

# # Fluxo condicional
# def decide_proximo_no(state: ConversationState):
#     tipo = state.tipo
#     if tipo == "vendas":
#         return "vendas"
#     elif tipo == "suporte":
#         return "suporte"
#     else:
#         print("❗ Entrada inválida, finalizando...")
#         return "finalizar"

# graph_builder.add_conditional_edges(
#     "pergunta",
#     decide_proximo_no,
#     {
#         "vendas": "vendas",
#         "suporte": "suporte",
#         "finalizar": "finalizar",
#     }
# )

# # Encaminha ambos os fluxos para o final
# graph_builder.add_edge("vendas", "finalizar")
# graph_builder.add_edge("suporte", "finalizar")
# graph_builder.add_edge("finalizar", END)

# # 4. Compilando o grafo
# graph = graph_builder.compile()

# # 5. Executando o grafo
# print("🚀 Iniciando execução do grafo...")
# result = graph.invoke(ConversationState())
# print("✅ Grafo executado com sucesso!")
# print(f"📊 Estado final: {result}")