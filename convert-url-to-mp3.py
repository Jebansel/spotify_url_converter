import os
from pytube import YouTube

# Function to download audio from YouTube URLs in a text file
def download_audio_from_youtube(text_file, output_folder):
    with open(text_file, 'r', encoding='utf-8') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace and newlines
            # Check if the URL matches the expected format
            if 'youtube.com' in url and 'watch?v=' in url:
                try:
                    yt = YouTube(url)
                    audio_stream = yt.streams.filter(only_audio=True).first()
                    audio_stream.download(output_folder)
                    # Rename the downloaded file to have the .mp3 extension
                    downloaded_file = os.path.join(output_folder, audio_stream.default_filename)
                    os.rename(downloaded_file, os.path.splitext(downloaded_file)[0] + '.mp3')
                    print(f"Downloaded audio from '{url}'")
                except Exception as e:
                    print(f"Error downloading audio from '{url}': {e}")
            else:
                print(f"Ignored invalid URL: '{url}'")


# Example usage
text_file = 'youtube_urls.txt'
output_folder = r'C:\Users\Jeban\Music\MP3s'
download_audio_from_youtube(text_file, output_folder)
