from datetime import datetime
from agents.models import ChatMessage, GraphState, Note
from langgraph.types import Command
from typing import List, Tuple
from langchain_openai import ChatOpenAI

class NoteLinkingAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fetch_note_content(self, graph_state: GraphState) -> Tuple[str, List[str]]:
        """
        Fetch the content of the note and existing note titles.
        """
        note_content = graph_state.generated_note.content
        note_titles = [note.title for note in Note.objects.all()]
        return note_content, note_titles

    def link_titles_in_content(self, content: str, titles: List[str]) -> str:
        """
        Add links for exact matches or similar matches in the content.
        """
        words = content.split()
        updated_content = []

        for word in words:
            # Check for exact match
            if word in titles:
                updated_content.append(f"[[ {word} ]]")
            else:
                # Use GPT to find similar matches
                prompt = (f"Given the word '{word}', find the most relevant title from the following list: {titles}. "
                          "If there is a strong match, return it; otherwise, return 'None'.")
                response = self.llm.call(prompt)
                similar_title = response.strip()
                if similar_title != 'None':
                    updated_content.append(f"[[ {similar_title} | {word} ]]")
                else:
                    updated_content.append(word)

        return " ".join(updated_content)

    def process_new_note(self, graph_state: GraphState) -> None:
        """
        Process the note content, linking titles, and update the note.
        """
        note_content, note_titles = self.fetch_note_content(graph_state)
        updated_content = self.link_titles_in_content(note_content, note_titles)
        
        # Update the generated note
        graph_state.generated_note.content = updated_content
        graph_state.generated_note.save()

    def link_new_note_title_in_existing_notes(self, new_note_title: str) -> None:
        """
        Search existing note contents for the new note title and add links.
        """
        existing_notes = Note.objects.all()

        for note in existing_notes:
            updated_content = self.link_titles_in_content(note.content, [new_note_title])
            if updated_content != note.content:
                note.content = updated_content
                note.save()

    def run(self, graph_state: GraphState) -> None:
        """
        Main execution logic for the agent.
        """
        # Process the current note content
        self.process_new_note(graph_state)

        # Link the new note title in existing notes
        new_note_title = graph_state.generated_note.title
        self.link_new_note_title_in_existing_notes(new_note_title)

# Usage example
if __name__ == "__main__":
    llm = ChatOpenAI()
    agent = NoteLinkingAgent(llm)

    # Assume `graph_state` is provided from the environment
    agent.run(graph_state)
