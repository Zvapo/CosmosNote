from agents.models import GraphState
from langchain_openai import ChatOpenAI
from tools.web_search_tool import web_search_tool
from tools.vector_search_tool import vector_search_tool
from tools.sql_agent import sql_tool
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command
from langchain_core.messages import AIMessage, SystemMessage
from agents.system_prompts import SystemPrompts
async def research_agent(state: GraphState, config: RunnableConfig):
    """
    This agent is responsible for interacting with tools and researching the query.
    """
    system_prompt = SystemMessage(content=SystemPrompts.ResearcherAgentPrompt)
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    search_tool_calls_count = len([True for x in filter(lambda x: isinstance(x, AIMessage), state["messages"]) if x['name'] == 'web_search_tool'])
    tools = [web_search_tool, vector_search_tool, sql_tool] if search_tool_calls_count < 3 else [vector_search_tool, sql_tool]
    llm_w_tools = llm.bind_tools(tools)

    messages = state["messages"]
    response = await llm_w_tools.ainvoke([system_prompt] + messages)

    return Command(
        update={
            "messages": [response],
        }
    )
