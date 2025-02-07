from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AgentDeps:  
    API_KEY: str = os.getenv("CHAT_API_KEY")