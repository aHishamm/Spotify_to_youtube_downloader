import spotipy
import os 
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
from pprint import pprint
from pytube import YouTube 
import datetime 
from youtube_search import YoutubeSearch
import gradio as gr 
def SpotifyBackend(cli_id,cli_secret,spotify_link):
    curr_directory = os.getcwd()
    lst = [] 
    youtube_video_list = [] 
    artist_name_List = [] 
    duration_List = [] 
    explicit_List = [] 
    track_name_list = [] 
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cli_id,
                                                               client_secret=cli_secret))
    offset=0
    while True: 
        response = sp.playlist_items(spotify_link,
                                     offset=offset,
                                     fields='items.track.name,items.track.explicit,items.track.duration_ms,items.track.artists.name',
                                     additional_types=['track']) 
        if len(response['items']) == 0: 
            break 
        lst.append(response['items']) 
        offset=offset+len(response['items']) 
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
        print("Song: "+str(i+1)+" link added.")
    spotify_df['links'] = youtube_video_list
    print(spotify_df)
    for i in range(len(spotify_df['links'])): 
        yt_link = YouTube(spotify_df['links'][i]) 
        print(yt_link)
        #condition to avoid 'streamingData' keyError 
        if(yt_link.age_restricted):
            continue
        stream_link = yt_link.streams.get_audio_only(subtype = "mp4")
        print("Song: "+str(i+1)+" downloaded.")
        stream_link.download(os.getcwd()+'/downloads') 
    return spotify_df

#UI 
with gr.Blocks() as demo: 
    with gr.Tab("First Tab"): 
        text_input1 = gr.Textbox(label='Credential ID') 
        text_input2 = gr.Textbox(label='Credential Secret')
        text_input3 = gr.Textbox(label='Spotify Playlist Link') 
        dataframe_output1 = gr.Dataframe() 
        button1 = gr.Button("Fetch Spotify Data") 
    button1.click(SpotifyBackend,inputs=[text_input1,text_input2,text_input3],
                  outputs=dataframe_output1)
demo.launch(share=True)