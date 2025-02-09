import os
import getpass
import json
from pathlib import Path
from dotenv import load_dotenv
from graph import Graph
import asyncio
from agents.models import GraphState
from langchain_core.messages import HumanMessage, AIMessage
from state_managment import _create_session_file, _load_session_state, _save_session_state, _generate_session_id
import uuid

# Load environment variables first
load_dotenv()

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

# Set required environment variables
_set_env("OPENAI_API_KEY")
_set_env("TAVILY_API_KEY")

async def main():
    graph = Graph()
    graph.save_graph_image()
    
    session_id = _generate_session_id()
    _create_session_file(session_id)
    
    TOOL_CALL_EVENT = 'on_tool_start'
    MESSAGE_EVENT = 'on_chat_model_stream'

    # Load or create session state
    session_state = {
        "user_prompt": "",
        "messages": [],
        "generated_note": None
    }

    config = {
        "configurable": {"thread_id": session_id}
    }

    async def process_message(user_input: str):
        session_state = _load_session_state(session_id)
        session_state["user_prompt"] = user_input
        session_state["messages"].append(HumanMessage(content=user_input))
        
        try:
            print("\nAssistant: ", end="", flush=True)  # Start response on new line
            
            async for event in graph.graph.astream_events(session_state, config, version="v1"):
                print('\nEvent: ', event['event'])
                if event['event'] == TOOL_CALL_EVENT:
                    print('TOOL Called: ', event['name'])
                elif event['event'] == MESSAGE_EVENT:
                    print(event)
                    # print(event['data']['chunk'].content, flush=True)
            
            _save_session_state(session_state, session_id)

        except Exception as e:
            print(f"\nError processing message: {e}")
            raise e

    # Main interaction loop
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            await process_message(user_input)
            
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())


