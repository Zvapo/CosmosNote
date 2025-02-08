from datetime import datetime
from agents.models import GraphState, ChatMessage
from langchain_openai import ChatOpenAI
from tools.web_search_tool import web_search_tool
from tools.vector_search_tool import vector_search_tool
from typing import Literal
from langgraph.types import Command

async def orchestrator_agent(state: GraphState) -> Command[Literal["sql_agent", "web_search_node", "vector_search_node"]]: # vector search tool, note making agent
    """
    This agent is responsible for replying to user prompt.
    This agent can use web search to find current information.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [web_search_tool, vector_search_tool] # add vector db tool, search tool
    llm.bind_tools(tools) # interface for the agent to know what tools are available
    
    user_message = state.user_prompt
    response = await llm.invoke(user_message)
    
    response_message = ChatMessage(
        role="assistant",
        content=str(response),
        timestamp=datetime.now().isoformat()
    )
    
    return {
        "conversation_history": [response_message],
        "user_prompt": state.user_prompt
    }





