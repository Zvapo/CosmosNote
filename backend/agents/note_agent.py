from agents.models import GraphState, Note
from langchain_openai import ChatOpenAI

def note_agent(state: GraphState):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    response = llm.with_structured_output(Note).invoke(state.messages) 
    print('the response of the note agent is', response)
    return { 
        "generated_note": response,
        }
