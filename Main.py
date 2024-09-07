import time

import yt_dlp
from features import *
from pytube import Search
from colorama import Fore
from pprint import pprint
import requests, os

def youtube_search(query):
    search = Search(query)
    results = search.results

    # Extract video titles and URLs
    videos = {}
    videos_names = []
    videos_urls = []

    for result in results:
        videos[result.title] = result.watch_url
        videos_names.append(result.title)
        videos_urls.append(result.watch_url)

    return videos, videos_names, videos_urls

def get_channel_name(channel_url):
    response = requests.get(channel_url)
    html = response.text
    channel_name = html.split('<title>')[1].split('</title>')[0]
    return channel_name.replace(' - YouTube', '')

def get_all_video_info(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    return info

def get_valid_data_channels(info, channel_name):
    Videos = {}
    VideosNames = []
    VideosPrewiews = {}

    Shorts = {}
    ShortsNames = []
    ShortsPrewiews = {}

    Lives = {}
    LivesNames = []
    LivesPrewiews = {}

    inp = False

    try:
        for i in range(len(info[f'{channel_name} - Videos']['entries'])):
            Videos[info[f'{channel_name} - Videos']['entries'][i]['title']] = info[f'{channel_name} - Videos']['entries'][i]['url']
            VideosPrewiews[info[f'{channel_name} - Videos']['entries'][i]['title']] = info[f'{channel_name} - Videos']['entries'][i]['thumbnails'][0]['url']
        pprint(Videos)
    except:
        os.system('cls')
        print_massage(Fore.RED + 'No videos' + Fore.RESET, 'ERROR', subtitle='[!]')

    try:
        for i in range(len(info[f'{channel_name} - Shorts']['entries'])):
            Shorts[info[f'{channel_name} - Shorts']['entries'][i]['title']] = info[f'{channel_name} - Shorts']['entries'][i]['url']
            ShortsPrewiews[info[f'{channel_name} - Shorts']['entries'][i]['title']] = info[f'{channel_name} - Shorts']['entries'][i]['thumbnails'][0]['url']
        pprint(Shorts)
    except:
        os.system('cls')
        print_massage(Fore.RED + 'No shorts' + Fore.RESET, 'ERROR', subtitle='[!]')

    try:
        for i in range(len(info[f'{channel_name} - Live']['entries'])):
            Lives[info[f'{channel_name} - Lives']['entries'][i]['title']] = info[f'{channel_name} - Lives']['entries'][i]['url']
            LivesPrewiews[info[f'{channel_name} - Lives']['entries'][i]['title']] = info[f'{channel_name} - Lives']['entries'][i]['thumbnails'][0]['url']
        pprint(Lives)
    except:
        os.system('cls')
        print_massage(Fore.RED + 'No live streams' + Fore.RESET, 'ERROR', subtitle='[!]')

    for k, v in Videos.items():VideosNames.append(k)
    for k, v in Shorts.items():ShortsNames.append(k)
    for k, v in Lives.items():LivesNames.append(k)

    return Videos, VideosNames, Shorts, ShortsNames, Lives, LivesNames, VideosPrewiews, ShortsPrewiews, LivesPrewiews

def download_video(url, name_of_exists_file=''):
    if name_of_exists_file == '':
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': '%(title)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': name_of_exists_file
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def get_channels():
    f = open('channels.txt', 'r')
    channels = f.read().split('\n')
    f.close()

    return channels

def channels():
    channels = {}
    channels_names = []
    for i in range(len(get_channels())):
        channels[get_channel_name(get_channels()[i])] = get_channels()[i]
        channels_names.append(get_channel_name(get_channels()[i]))

    while True:
        answer = menu(channels_names, addytube=True)
        print(answer)
        if answer == 'Back': break
        else:
            channel_url = channels[answer.replace('https://www.youtube.com/@', '')]
            channel_name = get_channel_name(channel_url)
            info = get_all_video_info(channel_url)
            All_videos = {}
            for video in info['entries']:
                All_videos[video['title']] = video
            valid_data = get_valid_data_channels(All_videos, channel_name)

            items = []

            if len(valid_data[0]) > 0:
                items.append('Videos')
            if len(valid_data[2]) > 0:
                items.append('Shorts')
            if len(valid_data[4]) > 0:
                items.append('Lives')

            answer = menu(items, question='Choose Category', addytube=False)
            while True:
                try:
                    back = False
                    if answer == 'Videos':
                        answer2 = menu(valid_data[1], question='Choose Short Video', addytube=False)
                        if answer2 == 'Back':
                            back = True
                        else:
                            print_image_2_console(valid_data[6][answer2])
                            wait()
                            answer3 = menu(['Download', 'Run'], question='Choose Action', addytube=False)
                            if answer3 == 'Download':
                                download_video(valid_data[0][answer2])
                            elif answer3 == 'Run':
                                os.system('mpv ' + valid_data[0][answer2])
                    elif answer == 'Shorts':
                        answer2 = menu(valid_data[3], question='Choose Video', addytube=False)
                        if answer2 == 'Back':
                            back = True
                        else:
                            print_image_2_console(valid_data[7][answer2])
                            wait()
                            answer3 = menu(['Download', 'Run'], question='Choose Action', addytube=False)
                            if answer3 == 'Download':
                                download_video(valid_data[2][answer2])
                            elif answer3 == 'Run':
                                os.system('mpv ' + valid_data[2][answer2])
                    elif answer == 'Lives':
                        answer2 = menu(valid_data[5], question='Choose Live', addytube=False)
                        if answer2 == 'Back':
                            back = True
                        else:
                            print_image_2_console(valid_data[8][answer2])
                            wait()
                            os.system('mpv ' + valid_data[4][answer2])
                    else:
                        break
                    if back: answer = menu(items, question='Choose Category', addytube=False)
                except Exception as err:
                    print(err)
                    wait(True, False)

def SearchYT():
    while True:
        print(Fore.BLUE + "[*]" + Fore.YELLOW + " To exit 'Search' enter 'Back' in search query..." + Fore.RESET)
        inp = input(Fore.BLUE + '[~]' + Fore.CYAN + ' Enter search query: ' + Fore.RESET)
        if inp == 'Back': break
        else:
            while True:
                videos, videos_names, videos_urls = youtube_search(inp)
                answer = menu(videos_names, addback=True, addytube=False)
                if answer == 'Back': break
                else:
                    answer3 = menu(['Download', 'Run'], question='Choose Action', addytube=False)
                    if answer3 == 'Download':
                        download_video(videos[answer])
                    elif answer3 == 'Run':
                        os.system('mpv ' + videos[answer])
                    else: continue

def main():

    while True:
        print_titles(['Youtube Client'])
        wait()

        while True:
            first_answer = menu(['Channels', 'Search'], addback=False, addytube=False)
            if first_answer == 'Channels': channels()
            elif first_answer == 'Search': SearchYT()

if __name__ == '__main__':
    main()