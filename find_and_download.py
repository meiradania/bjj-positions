from youtube_videos import youtube_search
from pytube import YouTube
import pandas as pd


def search_videos(search_term, n_results):
    res = youtube_search(q=search_term, max_results=n_results)
    token = res[0]
    videos = res[1]

    video_dict = {'youID': [], 'title': [], 'pub_date': [], 'channel': []}

    for video in videos:
        video_dict['youID'].append(video['id']['videoId'])
        video_dict['title'].append(video['snippet']['title'])
        video_dict['pub_date'].append(video['snippet']['publishedAt'])
        video_dict['channel'].append(video['snippet']['channelTitle'])

    print("added " + str(len(videos)) + " videos to a total of " + str(len(video_dict['youID'])))
    return video_dict


def search_and_save_data(bjj_term, first_n_results):
    df_yt = search_videos(bjj_term, first_n_results)
    try:
        df_yt.to_csv('files/' + bjj_term + '_' + first_n_results + '.csv')
    except FileNotFoundError:
        import os
        os.mkdir('files')
        df_yt.to_csv('files/' + bjj_term + '_' + first_n_results + '.csv')


def download_video(videoId):
    # https://python-pytube.readthedocs.io/en/latest/user/quickstart.html
    youtube_url = 'https://www.youtube.com/watch?v='
    yt = YouTube(youtube_url+videoId)

    # To query only first stream in the MPEG-4 format:
    stream = yt.streams.filter(file_extension='mp4').filter(res='240p').first()
    print(stream)
    if stream is not None:
        stream.download('/files')


def main(search_term_bjj, n_videos):
    search_and_save_data(search_term_bjj, n_videos)
    df_yt = pd.read_csv("files/" + search_term_bjj + n_videos + '.csv')
    df_yt['youID'].apply(download_video)

