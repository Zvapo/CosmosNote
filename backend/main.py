import os
import getpass
from dotenv import load_dotenv
from graph import Graph
import asyncio
from agents.models import GraphState
from langchain_core.messages import HumanMessage

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
        # Create initial state as a dictionary
        initial_state = {
            "user_prompt": user_input,
            "search_results": [],
            "messages": [HumanMessage(content=user_input)],
            "generated_note": None
        }
        
        try:
            # Use astream to get updates from all nodes
            async for output in graph.graph.astream(initial_state, {}):
                if output.get('messages'):
                    print('output', output['messages'][-1].content)

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


