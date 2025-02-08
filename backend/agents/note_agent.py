from agents.models import GraphState, Note
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage


def note_agent(state: GraphState):
    """
    This agent is responsible for generating a note based on the research results and the user prompt.
    """
    prompt = SystemMessage(content="""
        You are the Noting Agent in a multi-agent AI system dedicated to answering user questions about habitable planets in the universe.
        System Workflow Overview
            User Query: The user asks a question about habitable planets.
            Researcher Agent: You conduct thorough research based on available information sources.
            Noting Agent (Your Role): Receives your research and creates a structured note.
            Tagging Agent: Tags the note and stores it in the database.
            Response Agent: Uses the note to answer the user's question and generate three follow-up questions.
        Your Objective
            Your task is to create a note from the research recieved from the Researcher agent.
        Instructions
            In order to create a note, you need to follow these steps:
            1. Analyze the research and identify the key points.
            2. Create a structured note that is coherent and easy to understand.
        Output Requirements
            Deliver a note that is completly based on the research recieved from the Researcher agent.
            hand off the note to the Tagging Agent for further processing.
    """)
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    note = llm.with_structured_output(Note).invoke([prompt] + state["messages"])
    response = AIMessage(content="The note was generated successfully and saved to the state.")
    
    return {
        "generated_note": note,
        "messages": [response]
    }
