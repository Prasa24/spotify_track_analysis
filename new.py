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