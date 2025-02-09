# ExoMind

ExoMind is a research assistant that utilises an agentic swarm and a knowledge graph to facilitate research about exoplanets.
The swarm is made up of multiple agents working together to anwsers users research questions.
The results of the research are stored in an Obsidian Vault - a knowledge graph linking existing notes.
The information available to the swarm is stored in a vector database, a SQL database and a web-search tool.

This way an end-user has access to a verified database of information about exoplanets, and a constantly updating knowledge graph allowing the user to monitor the links between researched topics and access past research results at any time.

## Check out the website:

![ExoMind Demo](https://exomind.space)

## Check out the video of the demo:

<!-- <video src="backend/graphs_figs/demo.mp4" width="320" height="240" controls>
  Your browser does not support the video tag.
</video> -->

## Agentic Architecture

The swarm is made up of 4 main agents:

1. **Research Agent** - Searches available data sources for most relevant and up-to date information.
2. **Note Creation Agent** - Based on the search results creates a note summarising research findings.
4. **Note Linking Agent** - Links the notes in Obsidian Vault and the newly created note.
3. **Summary Agent** - Summarises the research findings in a concise and readibly manner for the user.

**The swarm is build using LangGraph:**

![LangGraph Architecture](backend/graphs_figs/graph.png)

## Features
- Access to a web-search tool
- Access to a vector database with research papers about exoplanets
- Access to a SQL database with numeric information from NASA's Expoplanet Archive
- Access to a Obsidian Vault as a knowledge graph

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/ExoMind-AI/ExoMind.git
cd ExoMind/backend
```
(https://github.com/syrianah)
```bash
# On Windows
venv\Scripts\activate
```

```bash
# On macOS/Linux 
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend:
```bash
python server.py
```

6. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

7. Run the frontend:
```bash
npm run dev
```

8. Navigate to the local host:
```bash
http://localhost:8000/
```

## Directory Structure

```bash

```

# The Team:

- [@Zvapo](https://github.com/Zvapo)
- [@wojtasmat](https://github.com/wojtasmat)
- [@JacobKaczmarek](https://github.com/JacobKaczmarek)
- [@syrianah](https://github.com/syrianah)

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.






