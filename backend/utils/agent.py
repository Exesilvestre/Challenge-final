
import json
import os
from cohere import ToolMessage
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from typing import Annotated, Literal, TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from utils.tools.get_dolar import get_dolar_hoy
from utils.tools.search_vector_db import search_vector_db

# Cargar variables de entorno si es necesario
load_dotenv()

tools = [get_dolar_hoy, search_vector_db]

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

llm = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"),              
                 model="command-r-plus-08-2024",
                 temperature=0)

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

class BasicToolNode:
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}
    
    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        print("Procesando herramientas con el mensaje:", message)
        outputs = []
        for tool_call in message.tool_calls:
            print("Llamando a la herramienta:", tool_call["name"])
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            print(f"Resultado de '{tool_call['name']}':", tool_result)
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}
    
tool_node = BasicToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
    
def route_tools(state: State) -> Literal["tools", "__end__"]:
    print("Estado recibido para routing:", state)
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        print("Herramienta detectada. Redirigiendo al nodo tools.")
        return "tools"
    
    print("No se detectaron herramientas. Finalizando flujo.")
    return "__end__"


graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", "__end__": "__end__"},
)

# Cada vez que usamos una funcion volvemos al chatbot paa que decida le proximo paso
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
    
def compile_and_save_graph():
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    print("Grafo compilado exitosamente.")
    print("Nodos en el grafo:", graph.nodes)
    return graph, memory

def llm_final_response(user_input, conversation_id):
    # Primero compilamos el grafo si es la primera vez que se invoca
    graph, memory = compile_and_save_graph()
    # Llamar al grafo para obtener la respuesta final
    final_state = graph.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": conversation_id}}
    )
    return final_state["messages"][-1].content