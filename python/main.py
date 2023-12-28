from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from datetime import timedelta

import os
import spotipy

if __name__ == "__main__":
    load_dotenv()

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            redirect_uri=os.environ.get("REDIRECT_URI"),
            scope='user-top-read user-read-recently-played'
        )
    )

    response = sp.current_user_recently_played()
    genres = []

    for item in response['items']:
        track = item['track']

        for artist in track['artists']:
            artist_info = sp.artist(artist['id'])
            genres += artist_info['genres']

            # print(f"Artist: {artist_name}, Genres: {genres}")
    
    genres = list(map(lambda genre: "-".join(genre.split(" ")), genres))
    genres = genres
    
    output_file_path = [os.path.join("data", "genres.txt"), os.path.join("data", "genres_30_days_assumption.txt")]

    with open(output_file_path[0], "w") as file:
        for item in genres:
            file.write(f"{item}\n")

    with open(output_file_path[1], "w") as file:
        for item in genres * 30:
            file.write(f"{item}\n")
    
    print(f"Data has been written to {output_file_path}")