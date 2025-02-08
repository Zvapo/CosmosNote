from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents import AgentType
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def sql_tool(query: str) -> str:
    """
    Query the database using natural language.
    Input should be a natural language question about the database.
    """
    DB_URI = os.getenv("DB_URI")
    db = SQLDatabase.from_uri(DB_URI)
    
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    return agent_executor.run(query)
