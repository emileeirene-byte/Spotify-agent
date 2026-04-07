# Spotify Taste Agent

A conversational AI agent that analyzes personal music taste and generates 
explained recommendations using a RAG architecture and LLM reasoning layer.

## What it does

- Pulls real listening data from the Spotify API (top artists, top tracks, 
  recently played)
- Stores it in a vector database (ChromaDB) for semantic retrieval
- Accepts natural language questions about music taste
- Returns reasoned analysis with specific pattern recognition
- Generates new artist recommendations with explained reasoning

## Architecture

**Retrieval layer:** ChromaDB vector database stores artist and track data 
as semantic embeddings. Queries return contextually relevant results rather 
than exact keyword matches.

**Prompt architecture:** Structured system prompt defines the agent's 
reasoning framework. The agent is instructed to identify patterns across 
genres, reference specific tracks, and show its reasoning rather than 
returning generic responses.

**LLM reasoning layer:** Claude claude-sonnet-4-20250514 receives the retrieved 
context and generates responses that explain the why behind taste patterns 
and recommendations.

**Data pipeline:** Spotify Web API -> JSON storage -> vector embeddings -> 
semantic query -> LLM reasoning -> conversational output.

## Example queries

- "What is my general music mood?"
- "Why do I gravitate toward certain artists?"
- "recommend" - generates 5 new artist recommendations with reasoning

## Setup

1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install spotipy python-dotenv chromadb anthropic`
5. Create a Spotify app at developer.spotify.com and get credentials
6. Get an Anthropic API key at console.anthropic.com
7. Create a `.env` file with your credentials (see `.env.example`)
8. Run `python auth.py` to authenticate with Spotify
9. Run `python fetch_data.py` to pull your listening data
10. Run `python agent.py` to start the agent

## Stack

- Python
- Spotify Web API + Spotipy
- ChromaDB
- Anthropic Claude API

