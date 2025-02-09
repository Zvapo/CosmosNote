# import json
# from pathlib import Path
# import uuid
# from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# # Create sessions directory if it doesn't exist
# SESSIONS_DIR = Path("session_data")
# SESSIONS_DIR.mkdir(exist_ok=True)

# def _generate_session_id():
#     return str(uuid.uuid4())

# def _load_session_state(session_id: str):
#     session_file = SESSIONS_DIR / f"session_{session_id}.json"
#     with open(session_file, 'r') as f:
#         data = json.load(f)
#         # Convert serialized messages back to Message objects
#         messages = []
#         for msg in data['messages']:
#             if msg['type'] == 'human':
#                 messages.append(HumanMessage(content=msg['content']))
#             elif msg['type'] == 'ai':
#                 messages.append(AIMessage(content=msg['content']))
#             elif msg['type'] == 'tool':
#                 messages.append(ToolMessage(content=msg['content'], tool_call_id=msg['tool_call_id']))
        
#         data['messages'] = messages
#         return data

# def _create_session_file(session_id: str = None):
#     session_file = SESSIONS_DIR / f"session_{session_id}.json"
#     if not session_file.exists():
#         session_state = {
#             "user_prompt": "",
#             "messages": [],
#             "generated_note": None
#         }
#         with open(session_file, 'w') as f:
#             json.dump(session_state, f, indent=2)
#     return session_file

# def _save_session_state(session_state: dict, session_id: str):
#     # Convert Message objects to a serializable format
#     serializable_state = session_state.copy()
#     messages = []
#     print('serializable_state', serializable_state)
#     for msg in serializable_state['messages']:
#         if isinstance(msg, HumanMessage):
#             message_dict = {
#                 'type': 'human',
#                 'content': msg.content
#             }
#         elif isinstance(msg, AIMessage):
#             message_dict = {
#                 'type': 'ai',
#                 'content': msg.content
#             }
#         elif isinstance(msg, ToolMessage):
#             message_dict = {
#                 'type': 'tool',
#                 'content': msg.content,
#                 'tool_call_id': msg.tool_call_id
#             }
#         else:
#             print(f"Unsupported message type: {type(msg)}")
#             continue
            
#         messages.append(message_dict)
    
#     serializable_state['messages'] = messages
    
#     session_file = SESSIONS_DIR / f"session_{session_id}.json"
#     with open(session_file, 'w') as f:
#         json.dump(serializable_state, f, indent=2)