from io import BytesIO
from PIL import Image
import os
from agents.models import GraphState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.summary_agent import summary_agent
from agents.note_agent import note_agent
from tools.sql_agent import sql_tool
from agents.research_agent import research_agent
from tools.web_search_tool import web_search_tool
from tools.vector_search_tool import vector_search_tool

class Graph:
    def __init__(self):
        self.graph_builder = StateGraph(GraphState)
        
        self.graph_builder.add_node("research_agent", research_agent)
        tools_node = ToolNode([web_search_tool, vector_search_tool, sql_tool])
        self.graph_builder.add_node("tools", tools_node)
        self.graph_builder.add_node("note_agent", note_agent)
        self.graph_builder.add_node("summary_agent", summary_agent)
        # Configure ToolNode with specific settings
        
        # Define edges
        self.graph_builder.add_edge(START, "research_agent")
        self.graph_builder.add_conditional_edges("research_agent", self.tools_router, ["tools", "note_agent"])
        self.graph_builder.add_edge("tools", "research_agent")
        self.graph_builder.add_edge("note_agent", "summary_agent")
        self.graph_builder.add_edge("summary_agent", END)
        
        # Compile the graph
        self.graph = self.graph_builder.compile()
    
    def save_graph_image(self):
        os.makedirs("graphs_figs", exist_ok=True)
        graph_bytes = self.graph.get_graph().draw_mermaid_png()
        
        buffer = BytesIO(graph_bytes)
        with Image.open(buffer) as img:
            img.save("graphs_figs/graph.png")
            
        print("Graph visualization saved to graphs_figs/graph.png")

    def tools_router(self, state: GraphState):
        messages = state.messages
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return "note_agent"

