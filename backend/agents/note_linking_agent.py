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
    print('note linking agent')
    prompt = SystemMessage(content=SystemPrompts.TaggingAgentPrompt)

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
        Update the note content so that it links to the "{state["generated_note"]["title"]}" note. A link to a note is formatted as [[{state["generated_note"]["title"]}]].
        If linking to a note would change the text of the note, use an alias [{state["generated_note"]["title"]} | source text]]. Do not change the content of the note, only add links.
        Do not add links that refer to the note itself.
        If you are unable to add a link, do not add any links.

        Current note:
        {existing_note}
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

