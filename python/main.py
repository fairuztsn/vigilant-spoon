from base64 import b64encode
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import requests
import json
import os

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

def get_token(authorization_code):
    auth_url = 'https://accounts.spotify.com/api/token'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {b64encode(f"{client_id}:{client_secret}".encode()).decode("utf-8")}',
    }
    
    payload = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'http://localhost:5000/callback',  # Use the same redirect_uri
        'scope': 'user-read-recently-played',  # Add the necessary scope
    }

    response = requests.post(auth_url, headers=headers, data=payload)
    return response.json()

def initiate_authorization():
    auth_url = 'https://accounts.spotify.com/authorize'
    redirect_uri = 'http://localhost:5000/callback'  # Replace with your actual redirect URI
    scope = 'user-read-recently-played'  # Add other scopes as needed

    authorization_url = (
        f"{auth_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}&state=STATE"
    )

    # Print or redirect to authorization_url to initiate the authorization process
    print("Visit the following URL to authorize, then copy the callback link to the next input\n", authorization_url)

def get_recently_played(access_token, limit=10):
    # Set up headers for the request
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Set up parameters for the request
    params = {
        'limit': limit,
    }

    # Make the initial request to get recently played tracks
    response = requests.get(
        'https://api.spotify.com/v1/me/player/recently-played',
        headers=headers,
        params=params,
    )

    # Process the response
    if response.status_code == 200:
        recently_played = response.json()
        items = recently_played.get('items', [])

        # If there are more results, fetch additional batches
        while recently_played.get('next'):
            # Get the next batch of recently played tracks
            response = requests.get(recently_played['next'], headers=headers)
            if response.status_code == 200:
                next_batch = response.json().get('items', [])
                items.extend(next_batch)
                recently_played = response.json()
            else:
                print(f"Error fetching next batch: {response.status_code} - {response.text}")
                break

        print(len(items))
        return items
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

def get_track_info(access_token):
    track_url = 'https://api.spotify.com/v1/tracks/4cOdK2wGLETKBW3PvgPWqT'

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(track_url, headers=headers)
    return response.json()

def get_auth_code_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    authorization_code = query_params.get('code', [None])[0]

    return authorization_code

def main():
    initiate_authorization()
    # Get access token
    token_response = get_token(get_auth_code_from_url(input("URL Callback: ")))

    # Check if access token was successfully obtained
    if 'access_token' in token_response:
        access_token = token_response['access_token']

        recently_played_tracks = get_recently_played(access_token, 50)

        # Print information about recently played tracks
        recently_played_data = []

        for item in recently_played_tracks:
            track = item.get('track', {})
            track_info = {
                'Track': track.get('name'),
                'Artist': track.get('artists', [{}])[0].get('name')
            }
            recently_played_data.append(track_info)

        # Specify the file path where you want to save the JSON data
        file_path = os.path.join("data", "recently_played_data.json")

        # Write the JSON data to the file with indentation
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(recently_played_data, json_file, indent=2, ensure_ascii=False)

        print(f"JSON data written to: {file_path}")

    else:
        print(f"Error: {token_response}")

if __name__ == "__main__":
    main()
