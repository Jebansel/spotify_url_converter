import csv
from googleapiclient.discovery import build
from urllib.parse import quote

def search_song_on_youtube(song_name, api_key):
    # Set up the YouTube Data API
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Construct the search query
    search_query = quote(song_name)
    
    # Make the API request to search for videos
    request = youtube.search().list(
        q=search_query,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()
    
    # Extract the video URL from the response
    if 'items' in response and response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return None

def find_youtube_urls(csv_file, api_key):
    youtube_urls = []

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            song_name = row[0]
            video_url = search_song_on_youtube(song_name, api_key)
            if video_url:
                youtube_urls.append([song_name, video_url])
            else:
                print(f"Song '{song_name}' not found on YouTube.")

    return youtube_urls

def write_to_csv(youtube_urls, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Song Name', 'YouTube URL'])
        writer.writerows(youtube_urls)

if __name__ == "__main__":
    csv_file = 'songs.csv'  # Path to your CSV file containing song names
    output_csv = 'youtube_urls.csv'  # Path to the output CSV file
    api_key = 'AIzaSyAvZn1GKg6f5jjnfWfhCnGCJFa2mD4xluE'  # Replace 'YOUR_API_KEY' with your actual YouTube Data API key
    youtube_urls = find_youtube_urls(csv_file, api_key)
    write_to_csv(youtube_urls, output_csv)
