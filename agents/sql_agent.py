import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langgraph.types import Command
from typing import Literal
from dotenv import load_dotenv

from state import GraphState

load_dotenv()


async def topic_agent(state: GraphState) -> Command[Literal["topic_agent"]]: 

    DB_URI = os.getenv("DB_URI")
    # Change from uri to connection string
    db = SQLDatabase.from_uri(DB_URI)

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    query = "What are the top 5 biggest exoplanets?"
    response = agent_executor.run(query)
    print(response)