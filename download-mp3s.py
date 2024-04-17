import requests
import csv
import re

# Function to search for a song on YouTube and return the URL
def search_song_on_youtube(song_name):
    # Perform a simple search on YouTube website
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    response = requests.get(search_url)
    if response.status_code == 200:
        # Extract the first video URL from the search results
        match = re.search(r'watch\?v=(\S{11})', response.text)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/watch?v={video_id}"
    return None

# Function to extract video ID from YouTube URL
def extract_video_id(youtube_url):
    pattern = r'(?<=v=)[\w-]+'
    match = re.search(pattern, youtube_url)
    if match:
        return match.group(0)
    else:
        return None

# Function to find YouTube URLs for songs listed in a CSV file
def find_youtube_urls(csv_file):
    youtube_urls = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            song_name = row[0]
            print(f"Searching for '{song_name}' on YouTube...")
            youtube_url = search_song_on_youtube(song_name)
            if youtube_url:
                print(f"Found YouTube URL for '{song_name}': {youtube_url}")
                youtube_urls.append(youtube_url)
            else:
                print(f"Song '{song_name}' not found on YouTube.")
    return youtube_urls

# Function to save YouTube URLs to a new TXT file
def save_youtube_urls_to_txt(youtube_urls, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for youtube_url in youtube_urls:
            file.write(youtube_url + '\n')


# Example usage
csv_file = 'songs.csv'
output_file = 'youtube_urls.txt'
youtube_urls = find_youtube_urls(csv_file)

# Save YouTube URLs to a TXT file
save_youtube_urls_to_txt(youtube_urls, output_file)
print("YouTube URLs saved to:", output_file)