from agents.models import GraphState
from langchain_openai import ChatOpenAI
from tools.web_search_tool import web_search_tool
from tools.vector_search_tool import vector_search_tool
from agents.sql_agent import sql_tool

async def orchestrator_agent(state: GraphState):
    """
    This agent orchestrates the flow and has access to all tools.
    Available tools:
    1. web_search_tool: Search the web for current information
    2. vector_search_tool: Search vector database for similar content
    3. sql_tool: Query the SQL database
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    # Make all tools available to the agent
    tools = [web_search_tool, vector_search_tool, sql_tool]
    llm_w_tools = llm.bind_tools(tools)

    response = await llm_w_tools.ainvoke(state.messages[-1].content)
    return {"messages": [response]}





