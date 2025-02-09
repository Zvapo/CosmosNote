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
    
    tool_calls_count = len([True for x in filter(lambda x: isinstance(x, AIMessage), state["messages"]) if x.tool_calls])
    
    if tool_calls_count >= 3:
        return Command(
            update={
                "messages": [AIMessage(content="INFORMATION_GATHERED")]
            }
        )
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, tags=["research_agent"])
    # max three searches for the agent to use
    tools = [web_search_tool, vector_search_tool, sql_tool]
    llm_w_tools = llm.bind_tools(tools)

    print(state["messages"])
    # count the number of web_search_tool tool calls
    search_tool_calls_count = len([True for x in filter(lambda x: isinstance(x, AIMessage), state["messages"]) if x.tool_calls])

    if search_tool_calls_count >= 3:
        response = AIMessage(content="INFORMATION_GATHERED")
    else:
        response = await llm_w_tools.ainvoke([system_prompt] + state["messages"])

    return Command(
        update={
            "messages": [response],
        }
    )
