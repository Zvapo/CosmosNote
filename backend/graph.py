from io import BytesIO
from PIL import Image
from agents.models import GraphState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.response_agent import orchestrator_agent
from agents.sql_agent import sql_agent
import os
from tools.web_search_tool import web_search_tool
from tools.vector_search_tool import vector_search_tool
class Graph:
    def __init__(self):
        self.graph_builder = StateGraph(GraphState)
        self.graph_builder.add_node("orchestrator_agent", orchestrator_agent)
        self.graph_builder.add_node("sql_agent", sql_agent)
        web_search_node = ToolNode([web_search_tool])
        vector_search_node = ToolNode([vector_search_tool])
        self.graph_builder.add_node("web_search_node", web_search_node)
        self.graph_builder.add_node("vector_search_node", vector_search_node)

        # Add entry point
        self.graph_builder.add_edge(START, "orchestrator_agent")
        self.graph_builder.add_edge("orchestrator_agent", "sql_agent")
        # self.graph_builder.add_edge("orchestrator_agent", "vector_search_node")

        self.graph_builder.add_edge("orchestrator_agent", END)
        
        # Compile with async config
        self.graph = self.graph_builder.compile()

    # def tool_router(self, state: GraphState) -> str:
    #     """Route to appropriate tool based on state"""
    #     if "use_web_search" in state and state.use_web_search:
    #         return "web_search_node"
    #     return "END"

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