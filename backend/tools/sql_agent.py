from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents import AgentType
import os
from dotenv import load_dotenv
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from agents.models import SearchResult
from langgraph.types import Command
from typing import Annotated
load_dotenv()

@tool
def sql_tool(query: str) -> str:
    """
    Query the database using natural language.
    Input should be a natural language question about the database.
    Your queries should follow the reasoning process of a human.
    This tool is used to search the database for information about exoplanets properties.
    The database contains information about exoplanets properties, such as the name, distance, mass, radius, etc.
    """
    print('HELLO FROM SQL TOOL')
    DB_URI = os.getenv("DB_URI")
    db = SQLDatabase.from_uri(DB_URI)
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent_executor.run(query)

