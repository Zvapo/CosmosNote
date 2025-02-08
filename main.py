from graph import Graph
from dotenv import load_dotenv
import asyncio
from agents.models import GraphState
import os

load_dotenv()

async def main():
    # Create graph instance
    graph = Graph()
    
    # Test prompt
    test_prompt = "Tell me about artificial intelligence."
    
    # Initial state
    initial_state = GraphState(conversation_history=[], user_prompt=test_prompt)
    
    # Stream responses
    print("\nProcessing responses:")
    print("-" * 50)
    

    # tutaj trzeba updatowac state z nowymi wiadomosciami od usera 
    async for event in graph.graph.astream(initial_state):
        # Process each state update
        for state_update in event.values():
            if not state_update:
                continue
            
            # Get the latest message from conversation history
            if "conversation_history" in state_update:
                latest_message = state_update["conversation_history"][-1]
                print(f"\n{latest_message.role}: {latest_message.content}")
                print("-" * 50)
    
    print("\nConversation complete!")

if __name__ == "__main__":
    asyncio.run(main())


