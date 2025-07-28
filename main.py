import os
from moviepy import VideoFileClip
from yt_dlp import YoutubeDL

VIDEO_DIR = "videos"
CLIP_LENGTH = 30  # saniye
CLIP_COUNT = 5    # kaç tane klip oluşturulacak

def download_video(youtube_url):
    os.makedirs(VIDEO_DIR, exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(VIDEO_DIR, '%(title)s.%(ext)s'),
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        print(f"Video indirildi: {filename}")
        return filename

def split_video_to_clips(video_path, clip_length=CLIP_LENGTH, clip_count=CLIP_COUNT):
    video = VideoFileClip(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    for i in range(clip_count):
        start_time = i * clip_length
        end_time = start_time + clip_length

        if end_time > video.duration:
            print("Video bitti, daha fazla klip çıkarılamaz.")
            break

        clip = video.subclipped(start_time, end_time)
        clip_path = os.path.join(VIDEO_DIR, f"{base_name}_clip{i+1}.mp4")
        clip.write_videofile(clip_path, codec="libx264")
        print(f"Klip {i+1} kaydedildi: {clip_path}")

if __name__ == "__main__":
    url = input("YouTube video linkini girin: ")
    video_path = download_video(url)
    split_video_to_clips(video_path)
