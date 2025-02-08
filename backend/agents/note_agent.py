from datetime import datetime
from agents.models import GraphState, Note
from langgraph.types import Command
from typing import Literal
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

def note_agent(state: GraphState):
    """
    This agent is responsible for generating a note based on the research results and the user prompt.
    """
    prompt = f"""
    Generate a note based on the research results and the user prompt. The note should be in the format of a markdown file.
    Research results: {state.conversation_history}
    User prompt: {state.user_prompt}
    """
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    response = llm.with_structured_output(Note).invoke(prompt)
    messages = [AIMessage(content="The note was generated successfully ansd saved to the state.")] 
    
    return {
        "generated_note": response,
        "messages": [messages]
    }
