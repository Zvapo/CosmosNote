from agents.models import GraphState
from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from agents.system_prompts import SystemPrompts

async def summary_agent(state: GraphState, config: RunnableConfig):
    """
    This agent is responsible for summarizing the research results and the flow of the application.
    """
    print('summary agent')
    system_prompt = SystemMessage(content=SystemPrompts.SummaryAgentPrompt)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, tags=["summary_agent"])
    response = llm.invoke([system_prompt] + state["messages"])
    return Command(
        update={
            "messages": [response]
        }
    )





