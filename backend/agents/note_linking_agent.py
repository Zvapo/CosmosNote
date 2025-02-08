from langchain_openai import ChatOpenAI
from agents.models import GraphState
from tools import file_writer_tool
from langchain_core.messages import AIMessage, SystemMessage
from langgraph.types import Command
from agents.system_prompts import SystemPrompts

def read_note(file_name: str):
    """
    Read note content from file.
    """
    try:
        with open(f"../quartz/content/{file_name}.md", "r") as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Error reading file {file_name}.md: {e}")
    
def write_note(file_name: str, content: str):
    """
    Write content to a file.
    """
    try:
        with open(f"../quartz/content/{file_name}.md", "w") as f:
            f.write(content)
        return f"File {file_name}.md written successfully."
    except Exception as e:
        raise Exception(f"Error writing file {file_name}.md: {e}")


def note_linking_agent(state: GraphState):
    """
    This agent is responsible for generating a note based on the research results and the user prompt.
    """

    prompt = SystemMessage(content=SystemPrompts.TaggingAgentPrompt)

    errors = []
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    response = llm.invoke(prompt)

    try:
        write_note(state.generated_note.name, response.content)
    except Exception as e:
        errors.append(f"Error writing note {state.generated_note.name}: {e}")

    for note in state.existing_notes:
        read_note(note)
        prompt = f"""
        Update the note content so that it links to the "{state.note.name}" note. A link to a note is formatted as [[{state.note.name}]].
        If linking to a note would change the text of the note, use an alias [[{state.note.name} | source text]]. Do not change the content of the note, only add links.
        If you are unable to add a link, do not add any links.

        Current note:
        {state.generated_note.content}
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

        state.note_titles = [state.generated_note.name]

    return Command(
        update={
            "messages": [AIMessage(content=output)]
        }
    )

