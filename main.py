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
    graph.save_graph_image()

    async def process_message(user_input: str):
        # Create initial state
        initial_state = {
            "conversation_history": [
                ChatMessage(
                    role="user",
                    content=user_input,
                    timestamp=datetime.now().isoformat()
                )
            ],
            "user_prompt": user_input
        }
        
        try:
            # Use ainvoke instead of stream for async operation
            result = await graph.graph.invoke(initial_state)
            
            # Process the result
            if result and "conversation_history" in result:
                latest_message = result["conversation_history"][-1]
                print(f"Assistant: {latest_message.content}")
        except Exception as e:
            print(f"Error processing message: {e}")

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


