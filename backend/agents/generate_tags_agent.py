from datetime import datetime
from agents.models import ChatMessage, GraphState
from langchain_openai import ChatOpenAI
from typing import Literal
from langgraph.types import Command


def tag_generation_agent(state: GraphState) -> Command[Literal["supervisor"]]:
    """
    This agent is responsible for generating relevant tags based on the content of the latest note in the graph state.
    """

    # Extract the latest note content from the state
    if not state.notes:
        return {
            "generated_tags": [],
            "conversation_history": [
                ChatMessage(
                    role="assistant", 
                    content="No notes available in the graph state to generate tags.",
                    timestamp=datetime.now().isoformat()
                )
            ]
        }

    latest_note = state.notes[-1].content

    # Define the prompt for tag generation
    prompt = f"""
    You are an expert in planetary science focusing on exoplanets and their habitability. Analyze the following note and identify 3 to 5 highly relevant tags.
    The tags should capture key themes, recurring factors influencing habitability (such as atmospheric composition, distance from the host star, and liquid water presence), and any notable findings.
    Ensure the tags are concise, specific, and aligned with the scientific aspects of planetary habitability.

    Note content: {latest_note}
    """

    # Initialize the LLM for tag generation
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # Invoke the LLM to generate the tags
    response = llm.invoke(prompt)

    # Ensure the response is a list of strings
    tags = response.split(', ') if isinstance(response, str) else []

    # Return the generated tags and conversation update
    return {
        "generated_tags": tags,
        "conversation_history": [
            ChatMessage(
                role="assistant", 
                content="The tags were generated successfully and saved to the state.",
                timestamp=datetime.now().isoformat()
            )
        ]
    }
