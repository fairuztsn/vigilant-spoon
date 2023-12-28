import csv
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import math

load_dotenv()

def transform_list(value):
    return [value+100, value+75, value+50, value+25, value, value, value-25, value-50, value-75, value-100]

def fetch_top_artists_and_time_per_artist(sp, limit):
    top_artists = sp.current_user_top_artists(time_range='short_term', limit=20)
    recently_played = sp.current_user_recently_played(limit=10)  # Fetch the most recently played track
    last_played_at_str = recently_played['items'][0]['played_at']

    # Convert the timestamp from string to datetime object
    last_played_at = datetime.strptime(last_played_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Calculate the total listening time in minutes based on the timestamp of the most recent track
    total_listening_time_minutes = (datetime.now() - last_played_at).total_seconds() / 60

    # Fetch genre information for each artist
    artists_with_time_and_genre = []

    for artist in top_artists['items']:
        artist_name = artist['name']

        # Query the Spotify API for artist details to get genres
        artist_details = sp.artist(artist['id'])
        genres = artist_details['genres'] if 'genres' in artist_details else []

        # Append the artist information to the list
        artists_with_time_and_genre.append({
            'artist': artist_name,
            'listening_time_minutes': int(math.ceil(total_listening_time_minutes)),
            'genres': genres
        })

    transformed_list = transform_list(artists_with_time_and_genre[0]["listening_time_minutes"])

    for i in range(len(artists_with_time_and_genre)):
        artists_with_time_and_genre[i]["listening_time_minutes"] = transformed_list[i]
    return artists_with_time_and_genre

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),
        redirect_uri=os.environ.get("REDIRECT_URI"),
        scope='user-top-read user-read-recently-played'
    )
)

top_artists_and_time = fetch_top_artists_and_time_per_artist(sp, limit=50)

csv_file_path = os.path.join("data", "top_artists_and_time_4_weeks.csv")
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['artist', 'listening_time_minutes', 'genres']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    for artist_info in top_artists_and_time:

        for i in range(len(artist_info['genres'])):
            artist_info['genres'][i] = "-".join(artist_info['genres'][i].split(" "))

        csv_writer.writerow({
            'artist': artist_info['artist'], 
            'listening_time_minutes': artist_info['listening_time_minutes'],
            'genres': ",".join(artist_info['genres'])
        })
        print(f"Artist: {artist_info['artist']}, Listening Time: {artist_info['listening_time_minutes']} minutes")

print(f"CSV file created: {csv_file_path}")