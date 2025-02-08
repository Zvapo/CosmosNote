from agents.models import GraphState
from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command
from langchain_core.messages import SystemMessage

async def summary_agent(state: GraphState, config: RunnableConfig):
    """
    This agent is responsible for summarizing the research results and the flow of the application.
    """
    system_prompt = SystemMessage(content="""
                                  You are a helpful assistant that can summarize the research results and the flow of the application.
                                  """)
    messages = state["messages"]
    messages[0] = system_prompt
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke(messages)
    return Command(
        update={
            "messages": [response]
        }
    )





