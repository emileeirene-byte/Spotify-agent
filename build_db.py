import json
import chromadb

with open("spotify_data.json") as f:
    data = json.load(f)

client = chromadb.Client()
collection = client.create_collection("music_taste")

documents = []
ids = []
metadatas = []

for i, artist in enumerate(data["top_artists"]):
    doc = "Artist: " + artist["name"]
    documents.append(doc)
    ids.append("artist_" + str(i))
    metadatas.append({"type": "artist", "name": artist["name"]})

for i, track in enumerate(data["top_tracks"]):
    doc = "Track: " + track["name"]
    doc += " by " + track["artists"][0]["name"]
    documents.append(doc)
    ids.append("track_" + str(i))
    metadatas.append({"type": "track", "name": track["name"]})

collection.add(documents=documents, ids=ids, metadatas=metadatas)

results = collection.query(query_texts=["emotional sad music"], n_results=5)
print("Query: emotional sad music")
for r in results["documents"][0]:
    print("  " + r)

