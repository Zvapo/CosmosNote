import os
import getpass
import json
from pathlib import Path
from dotenv import load_dotenv
from graph import Graph
import asyncio
from agents.models import GraphState
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
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
    def format_search_content(content):
        if content.keys() == ["content", "url"]:
            return f"{content["content"]} \n\n {content["url"]}"
        else:
            return content["content"]
        
    @staticmethod
    def format_event(message):
        if isinstance(message, AIMessage):
            if message.content == '':
                return None
            if message.content == 'INFORMATION_GATHERED':
                return None
            return {
                "status": "agent_message",
                "agent": '',
                "message": message.content
            }
        if isinstance(message, HumanMessage):
            if message.content == '':
                return None
            return {
                "status": "user_message",
                "message": message.content
            }
        if isinstance(message, ToolMessage):
            if message.content == '':
                return None
            return {
                "status": "tool_message",
                "name": SessionEvents.TOOLS_DICT[message.name],
                "message": SessionEvents.TOOLS_MESSAGE_DICT[message.name],
                "content": SessionEvents.format_search_content(message.content)
            }

        return None

async def main():
    graph = Graph()
    graph.save_graph_image()
    
    session_id = _generate_session_id()
    _create_session_file(session_id)
    
    TOOL_CALL_EVENT = 'on_tool_start'
    MESSAGE_EVENT = 'on_chat_model_stream'
    START_OUTPUT_EVENT = 'on_chat_model_start'

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
            async for event in graph.graph.astream(session_state, config):
                for state_update in event.values():
                    if not state_update:
                        continue

                    messages = state_update.get("messages", [])
                    if len(messages) > 0:
                        message = SessionEvents.format_event(messages[0])
                        if message:
                            print(message)
                

        except Exception as e:
            print(f"\nError processing event stream: {e}")

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


