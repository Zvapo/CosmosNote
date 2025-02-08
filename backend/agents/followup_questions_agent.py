from datetime import datetime
from agents.models import ChatMessage, GraphState, Note
from langgraph.types import Command
from typing import List
from langchain_openai import ChatOpenAI

class HabitablePlanetQuestionAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fetch_note_content(self, graph_state: GraphState) -> str:
        """
        Fetch the content of the newly created note.
        """
        return graph_state.generated_note.content

    def generate_follow_up_questions(self, note_content: str) -> List[str]:
        """
        Generate three follow-up questions based on the content of the note.
        """
        prompt = (f"Based on the following note content about habitable planets, generate three insightful follow-up questions: \n" 
                  f"Note Content: {note_content}\n" 
                  "Focus on scientific exploration and relevant details.")
        response = self.llm.call(prompt)
        questions = response.strip().split("\n")
        return questions[:3] if len(questions) >= 3 else questions

    def save_follow_up_questions(self, graph_state: GraphState, questions: List[str]) -> None:
        """
        Save the generated questions to the note.
        """
        graph_state.generated_note.follow_up_questions = questions
        graph_state.generated_note.save()

    def run(self, graph_state: GraphState) -> None:
        """
        Main execution logic for the agent.
        """
        # Fetch the note content
        note_content = self.fetch_note_content(graph_state)

        # Generate follow-up questions
        follow_up_questions = self.generate_follow_up_questions(note_content)

        # Save the generated questions
        self.save_follow_up_questions(graph_state, follow_up_questions)

# Usage example
if __name__ == "__main__":
    llm = ChatOpenAI()
    agent = HabitablePlanetQuestionAgent(llm)

    # Assume `graph_state` is provided from the environment
    agent.run(graph_state)
