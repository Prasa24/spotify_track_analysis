from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re

# Set up Client Credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='fe9cb27c79fa422da90d52c92f983981',
    client_secret='01e5f215840646eda60b896cdc71304e'
))

track_url="https://open.spotify.com/track/5yAfCVJwa3r9wAQSOfawqm"

# Extract track ID directly from URL using regex
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

#fetch track details
track=sp.track(track_id)
print(track) #will print as josn format 

#to extract meta data 
track_data={
    "Track name":track['name'],
    "Artists": " , ".join([artist['name'] for artist in track['artists']]),
    "Album":track['album']['name'],
    "Release Date":track['album']['release_date'],
    "Popularity":track['popularity'],
    "Track duration(minutes)":track['duration_ms']/60000
}

# Display metadata
print(f"\nTrack Name: {track_data['Track name']}")
print(f"Artists: {track_data['Artists']}")
print(f"Album: {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Track duration(minutes): {track_data['Track duration(minutes)']:.2f} minutes")
print(f"Release Date :{track['album']['release_date']}")

#metadata to dataframe 
df = pd.DataFrame([track_data])
print("\nTrack Data as DataFrame:")
print(df)

#save data to csv
df.to_csv('track_data.csv', index=False)

# Visualize track data
features = ['Popularity', 'Track duration(minutes)']
values = [track_data['Popularity'], track_data['Track duration(minutes)']]

plt.figure(figsize=(8, 5))
plt.bar(features, values, color='skyblue', edgecolor='black')
plt.title(f"Track Metadata for '{track_data['Track name']}'")
plt.ylabel('Value')
plt.show()