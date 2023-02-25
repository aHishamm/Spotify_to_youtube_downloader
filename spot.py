import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
from pprint import pprint 
lst = [] 
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="client_id",
                                                           client_secret="client_secret"))
offset=0
while True: 
    response = sp.playlist_items('https://open.spotify.com/playlist/0Z1vuQhvq7ghRieQurJIYg?si=7d85f27a390146a6',
                                 offset=offset,
                                 fields='items.track.name,items.track.explicit,items.track.duration_ms,items.track.artists.name',
                                 additional_types=['track']) 
    if len(response['items']) == 0: 
        break 
    #pprint(response['items']) 
    lst.append(response['items']) 
    offset=offset+len(response['items']) 
    #print(offset,"/",response['total'])
#artist name 
#print(lst[0][1]['track']['artists'][0]['name'])
#print(lst[0][1]['track']['duration_ms'])
artist_name_List = [] 
duration_List = [] 
explicit_List = [] 
track_name_list = [] 
for i in range(len(lst)): 
    for k in range(len(lst[i])): 
        artist_name_List.append(lst[i][k]['track']['artists'][0]['name'])
        duration_List.append(lst[i][k]['track']['duration_ms'])
        explicit_List.append(lst[i][k]['track']['explicit']) 
        track_name_list.append(lst[i][k]['track']['name'])
spotify_df = pd.DataFrame({'Artist_name':artist_name_List,
                           'Song_name':track_name_list,
                           'explicit':explicit_List,
                           'Song_duration':track_name_list}) 
#spotify_df.to_csv('spotify.csv',index=False)
