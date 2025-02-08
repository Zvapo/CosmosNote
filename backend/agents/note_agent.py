from agents.models import GraphState, Note
from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command

def note_agent(state: GraphState, config: RunnableConfig):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    print('\n hello my name is agent agent and this it what was passed')
    response = llm.with_structured_output(Note).invoke(state["messages"]) 
    print('the response of the note agent is', response)
    return Command(
        update={
            "generated_note": response
        }
    )

