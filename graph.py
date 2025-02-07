from io import BytesIO
from PIL import Image
from agents.models import GraphState
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents.response_agent import agent_0
import os

class GraphUtils:
    @staticmethod
    def save_graph_image(bytes_image, filename):
        buffer = BytesIO(bytes_image)
        
        with Image.open(buffer) as img:
            img.save(filename)


class Graph:
    def __init__(self):
        self.graph_builder = StateGraph(GraphState)
        self.graph_builder.add_node("agent_0", agent_0)
        self.graph_builder.set_entry_point("agent_0")
        self.graph_builder.add_edge("agent_0", END)
        
        # Compile without checkpointer
        self.graph = self.graph_builder.compile()

    def save_graph_image(self):
        os.makedirs("graphs_figs", exist_ok=True)
        buffer = BytesIO(self.graph.draw_mermaid_png())
        with Image.open(buffer) as img:
            img.save("graphs_figs/graph.png")