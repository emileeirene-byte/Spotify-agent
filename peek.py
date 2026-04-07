import json

with open("spotify_data.json") as f:
    data = json.load(f)

print("TOP ARTISTS:")
for a in data["top_artists"]:
    genres = a.get("genres", [])
    genre_str = ", ".join(genres[:3]) if genres else "no genres"
    print("  " + a["name"] + " - " + genre_str)

print("\nTOP TRACKS:")
for t in data["top_tracks"]:
    print("  " + t["name"] + " by " + t["artists"][0]["name"])