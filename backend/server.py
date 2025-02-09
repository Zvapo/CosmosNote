from fastapi import FastAPI, WebSocket
from graph import Graph
import json
import asyncio
from langchain_core.messages import HumanMessage
import uuid
from state_managment import _create_session_file, _load_session_state, _save_session_state, _generate_session_id

class SessionEvents:
    TOOL_CALL_EVENT = 'on_tool_start'
    MESSAGE_EVENT = 'on_chat_model_stream'
    START_OUTPUT_EVENT = 'on_chat_model_start'

    TOOLS_DICT = {
        "web_search_tool": "Web Search",
        "vector_search_tool": "Vector Search",
        "sql_tool": "SQL Query"
    }

    AGENT_NAMING_DICT = {
        "research_agent": "Renowned Exoplanet Researcher",
        "note_agent": "Scientific Journalist",
        "summary_agent": "Conclusion Writer"
    }

    @staticmethod
    def format_event(event, event_name:str):
        if event_name == SessionEvents.TOOL_CALL_EVENT:
            message = {
                "status": "tool_called",
                "name": SessionEvents.TOOLS_DICT[event['name']]
            }
            return message
        elif event_name == SessionEvents.MESSAGE_EVENT:
            if event['tags'][1] == 'note_linking_agent':
                return
            if event['data']['chunk'].content == '':
                return
            
            message = {
                "status": "message",
                "agent": SessionEvents.AGENT_NAMING_DICT[event['tags'][1]],
                "message": event['data']['chunk'].content
            }
            return message
        elif event_name == SessionEvents.START_OUTPUT_EVENT:
            if event['tags'][1] == 'note_linking_agent':
                return
            message = {
                "status": "start_chat",
                "agent": SessionEvents.AGENT_NAMING_DICT[event['tags'][1]]
            }
            return message


app = FastAPI()

@app.websocket("/ws/graph")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    graph = Graph()
    SAVE_SESSION_STATE = True # load session state from json file
    if SAVE_SESSION_STATE:
        session_id = _generate_session_id()
        _create_session_file(session_id)
    
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_json()
            await websocket.send_json(data)

            if SAVE_SESSION_STATE:
                session_state = _load_session_state(session_id)
            else:
                session_state = {
                    "user_prompt": data['user_prompt'], # need to get user prompt from
                    "messages": [HumanMessage(content=data['user_prompt'])]
                }
                config = {
                    "configurable": {"thread_id": session_id}
                }

            # Stream the graph execution
            try:
                async for event in graph.graph.astream_events(session_state, config, version="v1"):
                    message = SessionEvents.format_event(event, event['event'])
                    if message:
                        await websocket.send_json(message)

                    # save session state after graph execution
                    if SAVE_SESSION_STATE and event['event'] == 'on_chain_end':
                        saved_session_state = graph.graph.get_state(config)
                        _save_session_state(saved_session_state, session_id)

                # Send completion message after graph execution
                await websocket.send_json({
                     "status": "complete"
                })
                
            except Exception as e:
                print(e)
                await websocket.send_json({
                    "status": "error",
                    "message": f"Graph execution error: {str(e)}"
                })
                
    except Exception as e:
        print(e)
        await websocket.send_json({
            "status": "error",
            "message": f"WebSocket error: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 