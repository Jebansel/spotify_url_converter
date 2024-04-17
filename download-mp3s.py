import csv
import requests
from bs4 import BeautifulSoup

def search_song_on_youtube(song_name):
    # Construct the YouTube search URL
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    
    # Send a GET request to the search URL
    response = requests.get(search_url)
    
    # Parse the HTML content of the response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the first video link in the search results
    video_link = soup.find('a', {'class': 'yt-uix-tile-link'})
    
    if video_link:
        video_url = 'https://www.youtube.com' + video_link['href']
        return video_url
    else:
        return None

def find_youtube_urls(csv_file):
    youtube_urls = []

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            song_name = row[0]
            video_url = search_song_on_youtube(song_name)
            if video_url:
                youtube_urls.append([song_name, video_url])
            else:
                print(f"Song '{song_name}' not found on YouTube.")

    return youtube_urls

def save_youtube_urls(youtube_urls, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Song Name', 'YouTube URL'])
        writer.writerows(youtube_urls)

if __name__ == "__main__":
    csv_file = 'songs.csv'
    api_key = 'YOUR_YOUTUBE_API_KEY'  # Replace with your actual API key
    output_file = 'youtube_urls.csv'

    youtube_urls = find_youtube_urls(csv_file)
    save_youtube_urls(youtube_urls, output_file)
