import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
from pprint import pprint 
import datetime 
from youtube_search import YoutubeSearch
lst = [] 
youtube_video_list = [] 
artist_name_List = [] 
duration_List = [] 
explicit_List = [] 
track_name_list = [] 
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="",
                                                           client_secret=""))

offset=0
while True: 
    response = sp.playlist_items('https://open.spotify.com/playlist/1qC1eY5Z8W1eaCa6qcHwwa?si=ae92dca2fb6c4bef',
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
for i in range(len(lst)): 
    for k in range(len(lst[i])): 
        artist_name_List.append(lst[i][k]['track']['artists'][0]['name'])
        duration_List.append(lst[i][k]['track']['duration_ms'])
        explicit_List.append(lst[i][k]['track']['explicit']) 
        track_name_list.append(lst[i][k]['track']['name'])
spotify_df = pd.DataFrame({'Artist_name':artist_name_List,
                           'Song_name':track_name_list,
                           'explicit':explicit_List,
                           'Song_duration':duration_List}) 
spotify_df['Song_duration'] = spotify_df['Song_duration'].apply(lambda x: (str(datetime.timedelta(minutes=x/60000))[2:7]))
for i in range(len(spotify_df)): 
    result = YoutubeSearch(spotify_df["Artist_name"][i]+' - '+spotify_df["Song_name"][i],max_results=1).to_dict() 
    youtube_video_list.append('https://www.youtube.com'+result[0]['url_suffix']) 
print(youtube_video_list)
spotify_df['links'] = youtube_video_list
print(spotify_df)
#spotify_df.to_csv('spotify.csv',index=False)
