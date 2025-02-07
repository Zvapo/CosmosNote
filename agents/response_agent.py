from dataclasses import dataclass
from io import BytesIO
from PIL import Image
from uuid import uuid4
from datetime import datetime
from typing import List, Literal, Optional
from langgraph.types import Command
from pydantic_ai import Agent, RunContext
from agents.__init__ import AgentDeps
from state import GraphState
from agents.sql_agent import sql_agent

def format_conversation_history(state: GraphState):
    '''
    Helper function for formatting the conversation history.
    '''
    return f"Conversation history: {state.conversation_history}"

async def topic_agent(state: GraphState) -> Command[Literal["topic_agent"]]: 
    """
    This agent is responsible for replying to user prompt.
    This agent can use the following tools:
    - web_search
    - redirect to SQL agent
    - call to a vector database

    This agent will return a response to the user and to the Obsidian Note Agent.
    """

    topic_agent = Agent(
        model="gpt-4o-mini", # input model name
        system_prompt="", # add system prompt
        result_type=str, # outputs a simple response based on the prompt
        context=[format_conversation_history(state)],
        deps=AgentDeps()
    )

    response : str = await topic_agent.run()
    return Command(
        goto="note_agent", # go to research agent
        update={"last_response": response},
    )





