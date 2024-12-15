
import json
import os
from cohere import ToolMessage
from fastapi import requests
from langchain_cohere import ChatCohere
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from typing import Annotated, Literal, TypedDict
from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

@tool
def get_dolar_hoy():
    """
    Fetches the current exchange rate for the dollar from the API.
    This function makes a GET request to the 'dolarapi.com' API to retrieve
    the current exchange rate data.

    Returns:
        str: A string containing the current exchange rate of the dollar or an error message.
    """
    url = 'https://dolarapi.com/v1/dolares'
    try:
        response = requests.get(url)
        response.raise_for_status()
        dolar_data = response.json()
        return f"Dólar hoy: {dolar_data}"
    except requests.RequestException as e:
        return f"Error al obtener información del dólar: {str(e)}"
tool = get_dolar_hoy
tools = [tool]

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

llm = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"),              
                 model="command-r-plus-08-2024")

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage.

    This class retrieves tool calls from the most recent AIMessage in the input
    and invokes the corresponding tool to generate responses.

    Attributes:
        tools_by_name (dict): A dictionary mapping tool names to tool instances.
    """

    def __init__(self, tools: list) -> None:
        """Initializes the BasicToolNode with available tools.

        Args:
            tools (list): A list of tool objects, each having a `name` attribute.
        """
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        """Executes the tools based on the tool calls in the last message.

        Args:
            inputs (dict): A dictionary containing the input state with messages.

        Returns:
            dict: A dictionary with a list of `ToolMessage` outputs.

        Raises:
            ValueError: If no messages are found in the input.
        """
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}
    
tool_node = BasicToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)
    
def route_tools(
    state: State,
) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"

graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", "__end__": "__end__"},
)

# Cada vez que usamos una funcion volvemos al chatbot paa que decida le proximo paso
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")


def plot_agent_schema(graph):
    """Plots the agent schema using a graph object, if possible.

    Tries to display a visual representation of the agent's graph schema
    using Mermaid format and IPython's display capabilities. If the required
    dependencies are missing, it catches the exception and prints a message
    instead.

    Args:
        graph: A graph object that has a `get_graph` method, returning a graph
        structure that supports Mermaid diagram generation.

    Returns:
        None
    """
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        return print("Graph could not be displayed.")
    

def compile_and_save_graph():
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    return graph, memory

def llm_final_response(user_input, conversation_id):
    # Primero compilamos el grafo si es la primera vez que se invoca
    graph, memory = compile_and_save_graph()
    print(graph)
    for node in graph.nodes:
        print(node)
    # Llamar al grafo para obtener la respuesta final
    final_state = graph.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": conversation_id}}
    )
    return final_state["messages"][-1].content