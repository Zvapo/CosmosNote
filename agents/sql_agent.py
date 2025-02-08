<<<<<<< HEAD
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
=======
# agent to write sql queries and query the supabase database

class SystemPrompts:
    Agent0Prompt = """
        ##Instruction##
        You are one of the AI Agents in a program that structures research regarding habitable planets in the universe in a form of knowledge nodes. 
        You are working in a circular multi-agent workflow. 
        ---
        The first agent will answer questions regarding the topic of habitable planets according to sources like NASA exoplanets archive and other scientific sources. 
        ---
        The second agent will create a Knowledge Node.
        ---
        The third agent will give tags to the generate Knowledge Nodes in order to aggregate them.
        ---
        The forth agent will create 3 follow up questions.
        ---
        As the first agent your task is to act like a researcher of exoplanets and answer questions regarding the habitability of planets according to scientific sources 

        ##Desired format##
        You should give a comprehensive answer on the asked question. Provide the output as an answer
    """

    Agent1Prompt = """
    """
>>>>>>> 8546f1612c9ca012fc6484de76c836d9463feb53
