from bs4 import BeautifulSoup
import requests
from pathlib import Path
import youtube_dl
import pandas as pd
import os

def download_videos_from_titles(los):
    ids = []
    for index, item in enumerate(los):
        vid_id = scrape_vid_id(item)
        if vid_id:
            ids.append(vid_id)
    if ids:
        print("Downloading songs")
        download_videos_from_ids(ids)
    else:
        print("No valid video IDs found. Exiting.")

def download_videos_from_ids(lov):
    save_path = str(Path.home() / "Downloads/songs")
    try:
        os.makedirs(save_path, exist_ok=True)
    except OSError as e:
        print("Error creating download folder:", e)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': save_path + '/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(lov)
        except youtube_dl.utils.DownloadError as e:
            print("Download error:", e)

def scrape_vid_id(query):
    print("Getting video id for:", query)
    basic = "http://www.youtube.com/results?search_query="
    url = basic + query.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all('a', class_="yt-simple-endpoint style-scope ytd-video-renderer")
    if results:
        return results[0]['href'].split('/watch?v=')[1]
    else:
        print("Video not found for query:", query)
        return ''  # Return an empty string instead of None


def main():
    try:
        data = pd.read_csv('songs.csv')
        column_name = 'song names'  # Change this to the correct column name
        if column_name in data.columns:
            songs = data[column_name].tolist()
            print("Found", len(songs), "songs!")
            download_videos_from_titles(songs[0:1])
        else:
            print("Column", column_name, "not found in the CSV file.")
    except FileNotFoundError:
        print("Error: File 'songs.csv' not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()