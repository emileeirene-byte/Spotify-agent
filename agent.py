import json
import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

with open("spotify_data.json") as f:
    data = json.load(f)

client = chromadb.Client()
collection = client.create_collection("music_taste")

documents = []
ids = []

for i, artist in enumerate(data["top_artists"]):
    documents.append("Artist: " + artist["name"])
    ids.append("artist_" + str(i))

for i, track in enumerate(data["top_tracks"]):
    doc = "Track: " + track["name"] + " by " + track["artists"][0]["name"]
    documents.append(doc)
    ids.append("track_" + str(i))

collection.add(documents=documents, ids=ids)

scope = "user-top-read user-read-recently-played"
from spotipy.oauth2 import SpotifyOAuth
import spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

claude = anthropic.Anthropic()

def ask(question):
    global collection
    results = collection.query(query_texts=[question], n_results=5)
    context = "\n".join(results["documents"][0])
    
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system="""You are a music taste analyst. You have access to a user's 
real Spotify listening data. Analyze their taste thoughtfully and explain 
your reasoning. Be specific about patterns you notice. Be conversational.""",
        messages=[{
            "role": "user",
            "content": "My listening data:\n" + context + "\n\nQuestion: " + question
        }]
    )
    return response.content[0].text

def recommend():
    global collection
    top_names = [a["name"] for a in data["top_artists"][:10]]
    top_tracks = [t["name"] + " by " + t["artists"][0]["name"] 
                  for t in data["top_tracks"][:10]]
    
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system="""You are a music expert and taste analyst. Based on the 
user's listening data, recommend 5 artists they have never heard of. 
Be specific about why each recommendation fits their taste. 
Reference actual patterns from their listening history.""",
        messages=[{
            "role": "user",
            "content": "My top artists: " + ", ".join(top_names) +
                      "\n\nMy top tracks: " + ", ".join(top_tracks) +
                      "\n\nRecommend 5 new artists I should try and explain exactly why each one fits my taste."
        }]
    )
    return response.content[0].text

print("Spotify Agent ready. Commands: 'recommend', 'quit', or ask anything.\n")

while True:
    question = input("You: ")
    if question.lower() == "quit":
        break
    elif question.lower() == "recommend":
        print("\nAgent: " + recommend())
    else:
        print("\nAgent: " + ask(question))
    print()

