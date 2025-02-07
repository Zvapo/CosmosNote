from io import BytesIO
from PIL import Image
from state import GraphState
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class GraphUtils:
    @staticmethod
    def save_graph_image(bytes_image, filename):
        buffer = BytesIO(bytes_image)
        
        with Image.open(buffer) as img:
            img.save(filename)


class Graph:
    def __init__(self):
        self.memory = MemorySaver()
        self.graph_builder = StateGraph(GraphState)
        self.graph_builder.set_entry_point("topic_agent")
        self.graph_builder.add_edge("topic_agent", "research_agent")
        self.graph = self.graph_builder.compile(checkpointer=self.memory)

    def run(self):
        self.graph.invoke(
            {"first_prompt": "What is the meaning of life."}
        )

    def save_graph_image(self):
        buffer = BytesIO(self.graph.draw_mermaid_png())
        with Image.open(buffer) as img:
            img.save("graph.png")