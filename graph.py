from io import BytesIO
from PIL import Image
from agents.models import GraphState
from langgraph.graph import StateGraph, END
from agents.response_agent import response_agent
from agents.sql_agent import sql_agent
import os
from tools.web_search import web_search_tool

class Graph:
    def __init__(self):
        self.graph_builder = StateGraph(GraphState)
        self.graph_builder.add_node("response_agent", response_agent)
        self.graph_builder.add_node("sql_agent", sql_agent)
        
        self.graph_builder.set_entry_point("response_agent")
        self.graph_builder.add_edge("response_agent", END)
        
        # Compile with async config
        self.graph = self.graph_builder.compile()

    def save_graph_image(self):
        """
        Saves a visualization of the graph structure to a PNG file.
        """
        os.makedirs("graphs_figs", exist_ok=True)
        graph_bytes = self.graph.get_graph().draw_mermaid_png()
        
        buffer = BytesIO(graph_bytes)
        with Image.open(buffer) as img:
            img.save("graphs_figs/graph.png")
            
        print("Graph visualization saved to graphs_figs/graph.png")