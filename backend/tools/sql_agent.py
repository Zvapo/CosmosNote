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
def sql_tool(query: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """
    Query the database using natural language.
    Input should be a natural language question about the database.
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
    response = agent_executor.run(query)
    search_result = SearchResult(
        source='SQL Database',
        content=response
    )
    return Command(
        update={
            "messages": [ToolMessage(
                content=search_result.content, 
                tool_call_id=tool_call_id
            )],
            "search_results": [search_result]
        }
    )

