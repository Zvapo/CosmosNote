from agents.models import GraphState
from langchain_openai import ChatOpenAI

async def summary_agent(state: GraphState):
    """
    This agent is responsible for summarizing the research results and the flow of the application.
    """

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke(state.messages)
    return {"messages": [response]}





