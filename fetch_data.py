import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import json

load_dotenv()

scope = "user-top-read user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Top artists
top_artists = sp.current_user_top_artists(limit=20, time_range="medium_term")
# Top tracks
top_tracks = sp.current_user_top_tracks(limit=20, time_range="medium_term")
# Recently played
recent = sp.current_user_recently_played(limit=50)

data = {
    "top_artists": top_artists["items"],
    "top_tracks": top_tracks["items"],
    "recently_played": [item["track"] for item in recent["items"]]
}

with open("spotify_data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(data['top_artists'])} top artists")
print(f"Saved {len(data['top_tracks'])} top tracks")
print(f"Saved {len(data['recently_played'])} recent tracks")

