from datetime import datetime
from typing import Literal
from langgraph.types import Command
from pydantic_ai import Agent
from agents.__init__ import AgentDeps
from agents.models import GraphState, ChatMessage
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def format_conversation_history(state: GraphState):
    '''
    Helper function for formatting the conversation history.
    This message history can be passed to the agent as context.
    '''
    conversation_history = [f"{message.role} says {message.content}" for message in state.conversation_history]
    return "\n".join(conversation_history)

async def habitable_planet_tagger(state: GraphState):
    """
    This agent analyzes a note about habitable planets and generates tags.
    """
    topic_agent = Agent(
        model="gpt-4o-mini",
        system_prompt=(
            "You are a scientific assistant focused on exoplanet data. Analyze the following user note "
            "and generate relevant tags for indexing based on planetary characteristics, habitability factors, "
            "and scientific classification. Return tags as a comma-separated list."
        ),
        result_type=str,
    )

    run_result = await topic_agent.run(state.user_prompt)
    
    # Extract response from the RunResult object
    response_text = run_result._all_messages[1].parts[0].content
    
    # Cleanup tags if needed
    tags = [tag.strip() for tag in response_text.split(',') if tag.strip()]
    
    response_object = ChatMessage(
        role="agent", 
        content=", ".join(tags),
        timestamp=datetime.now().isoformat()
    )

    return {"conversation_history": [response_object]}
