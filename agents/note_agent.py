from datetime import datetime
from agents.models import ChatMessage, GraphState
from langgraph.types import Command
from typing import Literal
from langchain_openai import ChatOpenAI

def note_agent(state: GraphState) -> Command[Literal["supervisor"]]:
    """
    This agent is responsible for generating a note based on the research results and the user prompt.
    """
    prompt = f"""
    Generate a note based on the research results and the user prompt. The note should be in the format of a markdown file.
    Research results: {state.conversation_history}
    User prompt: {state.user_prompt}
    """
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    response = llm.invoke(prompt)

    return { "generated_note": response, "conversation_history": [ChatMessage(role="assistant", content="The note was generated successfully ansd saved to the state.", timestamp=datetime.now().isoformat())] }