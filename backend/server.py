from fastapi import FastAPI, WebSocket
from graph import Graph
import json
import asyncio

app = FastAPI()

@app.websocket("/ws/graph")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    graph = Graph()
    
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_json()

            await websocket.send_json(data)
            
            # Stream the graph execution
            try:
                async for message in graph.stream_run(data['user_prompt']):
                    # Convert message to JSON-serializable format
                    if hasattr(message, "to_dict"):
                        message = message.to_dict()
                    elif hasattr(message, "__dict__"):
                        message = message.__dict__
                        
                    await websocket.send_json({
                        "status": "streaming",
                        "message": message
                    })
                
                # Send completion message
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