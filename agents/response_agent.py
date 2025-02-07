from datetime import datetime
from typing import Literal
from langgraph.types import Command
from pydantic_ai import Agent
from agents.__init__ import AgentDeps
from agents.models import GraphState, ChatMessage
# from agents.sql_agent import sql_agent
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def format_conversation_history(state: GraphState):
    '''
    Helper function for formatting the conversation history.
    This message history can be passed to Agent 0 as context.
    '''
    conversation_history = ["{message.role} says {message.content}" for message in state.conversation_history]
    return "\n".join(conversation_history)

async def agent_0(state: GraphState):
    """
    This agent is responsible for replying to user prompt.
    This agent can use the following tools:
    - web_search
    - redirect to SQL agent
    - call to a vector database

    This agent will return a response to the user and to the Obsidian Note Agent.
    """
    topic_agent = Agent(
        model="gpt-4o-mini",
        system_prompt="You are a helpful AI assistant. Respond to the user's prompt.",
        result_type=str,
    )

    run_result = await topic_agent.run(state.user_prompt)
    
    # Extract response from the RunResult object
    # The response should be in the first text part of the response
    response_text = run_result._all_messages[1].parts[0].content
    
    response_object = ChatMessage(
        role="agent", 
        content=response_text,
        timestamp=datetime.now().isoformat()
    )

    return {"conversation_history": [response_object]}





