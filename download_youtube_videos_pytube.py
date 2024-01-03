import os

from pytube import YouTube


def download_youtube_video(url):
    try:
        # Create a YouTube object with the provided URL
        yt = YouTube(url)

        # Get the highest resolution stream available
        video_stream = yt.streams.get_highest_resolution()

        # Create output folder
        output_path = r'./videos'
        os.makedirs(output_path, exist_ok=True)

        # Download the video
        print(f"Downloading: {yt.title}...")
        video_stream.download(output_path=output_path)
        print("Download completed!")

        # Path of the downloaded video
        download_video_path = os.path.join(output_path, yt.title)
        return download_video_path

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


# Example URL of the YouTube video
video_url = "https://www.youtube.com/watch?v=h0uinE9oFVE"

# Call the function with the video URL
download_youtube_video(video_url)
