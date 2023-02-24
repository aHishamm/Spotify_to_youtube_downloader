import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
from pprint import pprint 

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="client_id",
                                                           client_secret="client_secret"))
offset=0
while True: 
    response = sp.playlist_items('https://open.spotify.com/playlist/0Z1vuQhvq7ghRieQurJIYg?si=7d85f27a390146a6',
                                 offset=offset,
                                 fields='items.track.name,total',
                                 additional_types=['track']) 
    if len(response['items']) == 0: 
        break 
    pprint(response['items']) 
    offset=offset+len(response['items']) 
    print(offset,"/",response['total'])
print(response)