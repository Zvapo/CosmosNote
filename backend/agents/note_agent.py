from agents.models import GraphState, Note
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage
from agents.system_prompts import SystemPrompts

def note_agent(state: GraphState):
    """
    This agent is responsible for generating a note based on the research results and the user prompt.
    """
    print('note agent')
    prompt = SystemMessage(content=SystemPrompts.NotingAgentPrompt)
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, tags=["note_agent"])
    note = llm.with_structured_output(Note).invoke([prompt] + state["messages"])
    response = AIMessage(content="The note was generated successfully and saved to the state.")
    
    return {
        "generated_note": note,
        "messages": [response]
    }
