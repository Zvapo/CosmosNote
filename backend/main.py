import os
import getpass
import json
from pathlib import Path
from dotenv import load_dotenv
from graph import Graph
import asyncio
from agents.models import GraphState
from langchain_core.messages import HumanMessage
import uuid

# Load environment variables first
load_dotenv()

# Create sessions directory if it doesn't exist
SESSIONS_DIR = Path("session_data")
SESSIONS_DIR.mkdir(exist_ok=True)

def _generate_session_id():
    return str(uuid.uuid4())

def _load_or_create_session(session_id: str = None):
    # Look for the most recent session file
    session_file = SESSIONS_DIR / f"session_{session_id}.json"
    if session_file.exists():
        with open(session_file, 'r') as f:
            return json.load(f), session_id
    
    # Create new session if none exists
    session_id = _generate_session_id()
    session_state = {
        "user_prompt": "",
        "search_results": [],
        "messages": [],
        "generated_note": None
    }
    return session_state, session_id

def _save_session_state(session_state: dict, session_id: str):
    # Convert HumanMessage objects to dictionary format for JSON serialization
    serializable_state = session_state.copy()
    serializable_state['messages'] = [
        {'type': 'human', 'content': msg.content} 
        if isinstance(msg, HumanMessage) 
        else msg 
        for msg in session_state['messages']
    ]
    
    session_file = SESSIONS_DIR / f"session_{session_id}.json"
    with open(session_file, 'w') as f:
        json.dump(serializable_state, f, indent=2)

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

# Set required environment variables
_set_env("OPENAI_API_KEY")
_set_env("TAVILY_API_KEY")

async def main():
    graph = Graph()
    graph.save_graph_image()
    
    # Generate a new session ID
    session_id = _generate_session_id()
    
    async def process_message(user_input: str):
        # Load session state with the generated session ID
        session_state, _ = _load_or_create_session(session_id)
        print('session_state', session_state)
        # Update session state
        session_state["user_prompt"] = user_input
        session_state["messages"].append(HumanMessage(content=user_input))
        
        try:
            # Use astream to get updates from all nodes
            async for output in graph.graph.astream(session_state, {}):
                if output.get('messages'):
                    print('output', output['messages'][-1].content)
            
            # Save updated session state after processing
            _save_session_state(session_state, session_id)

        except Exception as e:
            print(f"Error processing message: {e}")
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


