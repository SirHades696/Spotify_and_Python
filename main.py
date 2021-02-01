import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt

client_id = '' #client ID
client_secret = '' # Client secrect ID 

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id='' #Playlist ID
results = sp.playlist(playlist_id)

#Nombre de la playlist
playlist_name = results['name']

#track ID
songs_ids = []
for item in results['tracks']['items']:
    id = item['track']['id']
    songs_ids.append(id)


track_dict = {'id': [], 'name':[], 'artists':[], 'duration_ms':[], 'popularity':[]}

for id in songs_ids:
    data = sp.track(id)
    track_dict['id'].append(id)
    track_dict['name'].append(data['name'])
    track_dict['duration_ms'].append(data['duration_ms'])
    track_dict['popularity'].append(data['popularity'])
    separator = ', '
    name_artists = separator.join([artist['name'] for artist in data['artists']])
    track_dict['artists'].append(name_artists)

data_track = pd.DataFrame.from_dict(track_dict)
features = pd.DataFrame.from_dict(sp.audio_features(data_track['id']))
ft = features.get(['danceability', 'energy','loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'id' ])
all_data = data_track.merge(ft)
all_data['duration_ms']=all_data['duration_ms']/60000
desc = all_data.describe()
desc.plot.hist()
ft.plot.hist()
plt.show()



