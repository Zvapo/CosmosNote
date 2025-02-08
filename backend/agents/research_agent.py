from agents.models import GraphState
from langchain_openai import ChatOpenAI
from tools.web_search_tool import web_search_tool
from tools.vector_search_tool import vector_search_tool
from tools.sql_agent import sql_tool
from langchain.schema import SystemMessage


async def research_agent(state: GraphState):
    """
    This agent is responsible for interacting with tools and researching the query.
    """
    print('\n input to the agent', state)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    # max three searches for the agent to use
    if len(state.search_results) < 3:
        tools = [web_search_tool, vector_search_tool, sql_tool]
        llm_w_tools = llm.bind_tools(tools)
        response = await llm_w_tools.ainvoke(state.messages[-1].content)
    else:
        response = await llm.ainvoke(state.messages[-1].content)
    return { 
        "messages": [response]
        }
