import yt_dlp
import os

def download_youtube_video(url):
    output_dir = r'./videos'
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'merge_output_format': 'mp4',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            # Fetch the title from the downloaded video metadata
            video_title = info.get('title', 'Title Not Found')
            video_path = os.path.join(output_dir, video_title)
            return video_path
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading the video: {e}")
            return None