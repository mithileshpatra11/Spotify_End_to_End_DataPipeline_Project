import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import boto3
from datetime import datetime


def lambda_handler(event, context):
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    scope = "user-library-read"
    client_credentials_manager = SpotifyClientCredentials(client_id='client_id', client_secret='client_secret')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyClientCredentials())
    
    playlists = sp.user_playlists('spotify')
    playlist_link = 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF'
    playlist_URI = playlist_link.split('/')[-1]
    data = sp.playlist_tracks(playlist_URI)
    
    client = boto3.client('s3')
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    client.put_object(
        Bucket="spotify-etl-project-hony",
        Key="raw_data/to_process/" + filename,
        Body=json.dumps(data)
        )