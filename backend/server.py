from fastapi import FastAPI, WebSocket
from graph import Graph
from langchain_core.messages import HumanMessage
from state_managment import _create_session_file, _load_session_state, _save_session_state, _generate_session_id
from dotenv import load_dotenv
import os
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

load_dotenv()

class SessionEvents:
    TOOL_CALL_EVENT = 'on_tool_start'
    MESSAGE_EVENT = 'on_chat_model_stream'
    START_OUTPUT_EVENT = 'on_chat_model_start'

    TOOLS_DICT = {
        "web_search_tool": "Web Search",
        "vector_search_tool": "Vector Search",
        "sql_tool": "SQL Query"
    }

    TOOLS_MESSAGE_DICT = {
        "web_search_tool": "Searching the web for information...",
        "vector_search_tool": "Searching the vector database for information...",
        "sql_tool": "Executing a SQL query..."
    }

    AGENT_NAMING_DICT = {
        "research_agent": "Renowned Exoplanet Researcher",
        "note_agent": "Scientific Journalist",
        "summary_agent": "Conclusion Writer"
    }

    @staticmethod
    def format_event(message):
        if isinstance(message, AIMessage):
            return {
                "status": "agent_message",
                "agent": '',
                "message": message.content
            }
        if isinstance(message, HumanMessage):
            return {
                "status": "user_message",
                "message": message.content
            }
        if isinstance(message, ToolMessage):
            return {
                "status": "tool_message",
                "name": SessionEvents.TOOLS_DICT[message.name],
                "message": SessionEvents.TOOLS_MESSAGE_DICT[message.name]
            }

        return None


app = FastAPI()

@app.websocket("/ws/graph")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    graph = Graph()
    SAVE_SESSION_STATE = False # load session state from json file
    session_id = _generate_session_id()
    if SAVE_SESSION_STATE:
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
                async for event in graph.graph.astream(session_state, config):
                    for state_update in event.values():
                        if not state_update:
                            continue

                        messages = state_update.get("messages", [])
                        if len(messages) > 0:
                            message = SessionEvents.format_event(messages[0])
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
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 8000))