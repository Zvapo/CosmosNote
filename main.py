import os
import getpass
from dotenv import load_dotenv
from graph import Graph
import asyncio
from agents.models import GraphState, ChatMessage
from datetime import datetime

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

    async def stream_graph_updates(user_input: str):
        initial_state = GraphState(
            conversation_history=[
                ChatMessage(
                    role="user",
                    content=user_input,
                    timestamp=datetime.now().isoformat()
                )
            ],
            user_prompt=user_input
        )
        
        async for event in graph.graph.astream(initial_state.model_dump()):
            for value in event.values():
                if value and "conversation_history" in value:
                    latest_message = value["conversation_history"][-1]
                    print(f"Assistant: {latest_message.content}")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            await stream_graph_updates(user_input)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())


