from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from datetime import timedelta

import os
import spotipy

def get_top_artists(sp: SpotifyOAuth, time_range: str) -> list:
    print("get_top_artists")
    if not (time_range in ["short_term", "medium_term", "long_term"]):
        raise ValueError("Unknown time range")
    
    genres = []
    artists = []
    top_artists = sp.current_user_top_artists(limit=20, time_range=time_range)

    for item in top_artists["items"]:
        genres += item["genres"]
        artists.append(item["name"])

    return dict(genres=genres, artists=artists)

def get_top_tracks(sp: SpotifyOAuth, time_range: str) -> list:
    print("get_top_tracks")
    if not(time_range in ["short_term", "medium_term", "long_term"]):
        raise ValueError("Unknown time range")
    
    genres = []
    artists = []

    top_tracks = sp.current_user_top_tracks(limit=20, time_range=time_range)

    for item in top_tracks["items"]:
        for artist in item["artists"]:
            artist_info = sp.artist(artist["id"])
            genres += artist_info["genres"]
            artists.append(artist_info["name"])
    
    return dict(genres=genres, artists=artists)

def write_to_txt(genres: list, artists: list) -> None:
    print("write_to_txt")
    output_file_path = {
        "genres": [os.path.join("data", "genres.txt"), os.path.join("data", "genres_30_days_assumption.txt")],
        "artists": os.path.join("data", "artists.txt")
    }

    with open(output_file_path["genres"][0], "w") as file:
        for item in genres:
            file.write(f"{item}\n")

    with open(output_file_path["genres"][1], "w") as file:
        for item in genres * 30:
            file.write(f"{item}\n")

    with open(output_file_path["artists"], "w", encoding="utf-8") as file:
        for item in artists:
            file.write(f"{item}\n")
    
    print(f"Data has been written to: {output_file_path}")

def generate() -> None:
    load_dotenv()

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            redirect_uri=os.environ.get("REDIRECT_URI"),
            scope='user-top-read user-read-recently-played',
            state=None,
            cache_handler=spotipy.CacheFileHandler()
        )
    )

    response = sp.current_user_recently_played(limit=50)
    genres = []
    artists = []

    for item in response['items']:
        track = item['track']

        for artist in track['artists']:
            try:
                artist_info = sp.artist(artist['id'])
            except spotipy.SpotifyException as e:
                print(f"Error fetching artist info: {e}")
                
            artists.append(artist["name"])
            genres += artist_info['genres']

            # print(f"Artist: {artist_name}, Genres: {genres}")
    
    time_ranges = ["short_term", "medium_term", "long_term"]

    for time_range in time_ranges:
        print("Looping time range")
        top_artists = get_top_artists(sp, time_range=time_range)
        top_tracks = get_top_tracks(sp, time_range=time_range)
        genres += top_artists["genres"]
        genres += top_tracks["genres"]

        artists += top_artists["artists"]
        artists += top_tracks["artists"]

    genres = list(map(lambda genre: "-".join(genre.split(" ")), genres))
    artists = list(map(lambda artist: "_".join(artist.split(" ")), artists))

    write_to_txt(genres, artists)

if __name__ == "__main__":
    artist_file = os.path.join("data", "artists.txt")

    with open(artist_file, "r", encoding="utf-8") as file:
        content = file.read()

    artists = content.split("\n")
    artists = map(lambda artist: "_".join(artist.split(" ")), artists)
    
    with open(artist_file, "w", encoding="utf-8") as file:
        for artist in artists:
            file.write(artist + "\n")