from fastapi import FastAPI, WebSocket
from graph import Graph
import json
import asyncio
from langchain_core.messages import HumanMessage
import uuid


app = FastAPI()

@app.websocket("/ws/graph")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    graph = Graph()
    
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_json()
            session_id = str(uuid.uuid4())

            await websocket.send_json(data)
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
                    if event['event'] == 'on_tool_start':
                        await websocket.send_json({
                            "status": "tool_called",
                            "tool_name": event['name']
                        })
                    elif event['event'] == 'on_chat_model_stream':
                        chat_message = event['data']['chunk'].content
                        # some chat messages are empty and no streaming of note_linking_agent
                        if chat_message != '' and 'note_linking_agent' not in event['tags']:
                            await websocket.send_json({
                                "status": "message",
                                "message": chat_message
                            })
                
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