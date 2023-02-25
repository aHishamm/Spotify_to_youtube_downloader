import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import googleapiclient.discovery
import pandas as pd 
from pprint import pprint 
import datetime 
from youtube_search import YoutubeSearch
#from pytube import Search 
api_service_name = 'youtube'
api_version = "v3"
dev_key = ''
lst = [] 
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="",
                                                           client_secret=""))

yt = googleapiclient.discovery.build(api_service_name,api_version,developerKey="")
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
                           'Song_duration':duration_List}) 
spotify_df['Song_duration'] = spotify_df['Song_duration'].apply(lambda x: (str(datetime.timedelta(minutes=x/60000))[2:7]))


results = YoutubeSearch('Rain City Drive Heavier', max_results=10).to_json()
print(results)
#print(spotify_df)
#print(spotify_df['Artist_name'][0]+' '+spotify_df['Song_name'][0])
#spotify_df.to_csv('spotify.csv',index=False)


#request to youtube API 
#request = yt.search().list(
#    part='snippet',
#    q='Rain City Drive Heavier',
#    maxResults=3,
#    order='viewCount',
#    type='video' 
#)
#response_yt = request.execute() 
#print(response_yt['items'][0]['id']['videoId'])

#youtube_video_list = [] 
#for i in range(200): 
#    #print(spotify_df['Artist_name'][i]+' - '+spotify_df['Song_name'][i])
#    request = yt.search().list(
#    part='snippet',
#    q=spotify_df["Artist_name"][i]+' - '+spotify_df["Song_name"][i],
#    maxResults=1,
#    order='viewCount',
#    type='video' 
#    )
#    response_yt = request.execute() 
#    youtube_video_list.append(response_yt['items'][0]['id']['videoId'])
#
#print(youtube_video_list)
#spotify_df['links'] = youtube_video_list
#spotify_df.to_csv('spotify.csv',index=False)
