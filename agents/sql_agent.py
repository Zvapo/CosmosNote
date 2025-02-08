import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from typing import Literal
from dotenv import load_dotenv
from agents.models import GraphState

load_dotenv()


def sql_agent(state: GraphState) -> Command[Literal["supervisor"]]:
    """
    This agent is responsible for querying the database.
    """
    DB_URI = os.getenv("DB_URI")
    db = SQLDatabase.from_uri(DB_URI)

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    response = agent_executor.run(state.conversation_history)

    return { "conversation_history": [response] }
