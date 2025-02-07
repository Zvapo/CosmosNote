from dataclasses import dataclass
from io import BytesIO
from PIL import Image
from uuid import uuid4
from datetime import datetime
from typing import List, Literal, Optional
from langgraph.types import Command
from pydantic_ai import Agent, RunContext

from state import GraphState

@dataclass
class AgentDeps:  
    entry_prompt: str

async def topic_agent(state: GraphState) -> Command[Literal["topic_agent"]]: 
    """
    This agent is responsible for generating three questions from a given note or prompt.
    """

    if state.first_run:
        deps = AgentDeps(entry_prompt=state.first_prompt)
    else:
        deps = AgentDeps(entry_prompt=state.notes[-1])

    topic_agent = Agent(
        model="gpt-4o-mini", # input model name
        system_prompt="", # add system prompt
        result_type=List[str], # output 3 pytania
        deps=deps
    )

    questions : List[str] = await topic_agent.run()
    return Command(
        goto="research_agent", # go to research agent
        update={"research_questions": questions},
    )





