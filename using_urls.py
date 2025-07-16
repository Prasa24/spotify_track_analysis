import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
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

# Read track URLs from file
file_path = "track_urls.txt"
with open(file_path, 'r') as file:
    track_urls = file.readlines()

# Process each URL
for track_url in track_urls:
    track_url = track_url.strip()  # Remove any leading/trailing whitespace
    try:
        # Extract track ID from URL
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

        # Fetch track details from Spotify API
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
        VALUES (%s, %s, %s, %s, %s,%s)
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

        print(f"Inserted: {track_data['Track name']} by {track_data['Artists']}")

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

# Close the connection
cursor.close()
connection.close()

print("All tracks have been processed and inserted into the database.")