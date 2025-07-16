import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='fe9cb27c79fa422da90d52c92f983981',  
    client_secret='01e5f215840646eda60b896cdc71304e'
)) 
# MySQL Database Connection
db_config = {
    'host': 'localhost',         
    'user': 'root',       
    'password': '12345678',   
    'database': 'for_spotify'       
}
# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Full track URL (example: Shape of You by Ed Sheeran)
track_url = "https://open.spotify.com/track/5yAfCVJwa3r9wAQSOfawqm"

# Extract track ID directly from URL
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

# Fetch track details
track = sp.track(track_id)

# Extract metadata
track_data={
    "Track name":track['name'],
    "Artists": " , ".join([artist['name'] for artist in track['artists']]),
    "Album":track['album']['name'],
    "Release Date":track['album']['release_date'],
    "Popularity":track['popularity'],
    "Track duration(minutes)":track['duration_ms']/60000
}

# Insert data into MySQL
insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album,release_date, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s , %s)
"""
cursor.execute(insert_query, (
    track_data['Track name'],
    track_data['Artists'],
    track_data['Album'],
    track_data['Release Date'],
    track_data['Popularity'],
    track_data['Track duration(minutes)']
))
connection.commit()

print(f"Track '{track_data['Track name']}' by {track_data['Artists']} inserted into the database.")

# Close the connection
cursor.close()
connection.close()