from agents.models import GraphState, Note
from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command
from langchain_core.messages import SystemMessage

def note_agent(state: GraphState, config: RunnableConfig):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    system_prompt = SystemMessage(content="""
                                  You are a helpful assistant that can generate a note about the information you find.
                                  """)
    
    messages = state["messages"]
    call_messages = messages.copy() # do not save the system prompt in the state
    call_messages[0] = system_prompt
    response = llm.with_structured_output(Note).invoke(call_messages) 
    return Command(
        update={
            "generated_note": response
        }
    )

