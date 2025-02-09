from langchain_openai import ChatOpenAI
from agents.models import GraphState
from tools import file_writer_tool
from langchain_core.messages import AIMessage, SystemMessage
from langgraph.types import Command
from agents.system_prompts import SystemPrompts
import os
from pathlib import Path

# Get the absolute path to the quartz/content directory
CONTENT_DIR = Path(__file__).parent.parent / "quartz" / "content"

def read_note(file_name: str):
    """
    Read note content from file.
    """
    try:
        file_path = CONTENT_DIR / f"{file_name}.md"
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Error reading file {file_name}.md: {e}")

def list_notes():
    """
    List all notes in the content directory.
    """
    try:
        return [f.stem for f in CONTENT_DIR.glob("*.md")]
    except Exception as e:
        raise Exception(f"Error listing notes: {e}")

def write_note(file_name: str, content: str):
    """
    Write content to a file.
    """
    try:
        # Ensure the content directory exists
        CONTENT_DIR.mkdir(parents=True, exist_ok=True)
        
        file_path = CONTENT_DIR / f"{file_name}.md"
        print("Writing to file: ", file_path)
        with open(file_path, "w") as f:
            f.write(content)
        return f"File {file_name}.md written successfully."
    except Exception as e:
        raise Exception(f"Error writing file {file_name}.md: {e}")


def note_linking_agent(state: GraphState):
    """
    This agent is responsible for generating a note based on the research results and the user prompt.
    """
    existing_notes = list_notes() 
    prompt = SystemMessage(content=SystemPrompts.TaggingAgentPrompt.invoke({"existing_notes_content": existing_notes, "note": state["generated_note"]["content"]}))

    errors = []
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, tags=["note_linking_agent"])

    response = llm.invoke([prompt] + state["messages"])

    try:
        write_note(state["generated_note"]["title"], response.content)
    except Exception as e:   
        errors.append(f"Error writing note {state['generated_note']['title']}: {e}")

    for note in list_notes():
        existing_note = read_note(note)
        prompt = f"""

        Your job is to take the newly saved note title and check for it occurences in every note.
        If you find any similar or equal words in one of the existing notes, update it in the following way:
                if the word is exactly the same, add "[[" before the word and "]]" after the word.                                    
                if the word is similar, change the word to "[[ the matching saved note title | current note word]]".
               
        Current note title: 
            {state["generated_note"]["title"]}
        Output Requirements: 
           You should return the updated note content.
        
        """

        response = llm.invoke(prompt)

        try:
            write_note(note, response.content)
        except Exception as e:
            errors.append(f"Error writing note {note}: {e}")

    if len(errors) > 0:
        output = f"Errors: {errors}"
    else:
        output = "Linking successful."

    return Command(
        update={
            "messages": [AIMessage(content=output)]
        }
    )

