# import os
# from langchain_openai import ChatOpenAI
# from models import GraphState, Note
# from datetime import datetime


# async def note_agent(state: GraphState):
#     """
#     This agent is responsible for replying to user prompt.
#     This agent can use web search to find current information.
#     """
#     llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#     llm.with_structured_output(Note).invoke()
#     note = Note(
#         title="",
#         content="",
#         tags=[],
#         follow_up_questions=[]
#     )

#     return {"conversation_history": [response_object]}