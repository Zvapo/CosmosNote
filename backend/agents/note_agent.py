from agents.models import GraphState, Note
from langchain_openai import ChatOpenAI

def note_agent(state: GraphState):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    print('\n hello my name is agent agent and this it what was passed', state.messages[-1].content)
    response = llm.with_structured_output(Note).invoke(state.messages[-1].content) 
    print('the response of the note agent is', response)
    return { 
        "generated_note": response,
        }
