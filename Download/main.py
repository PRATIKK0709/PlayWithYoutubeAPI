from pytube import YouTube
from tqdm import tqdm

def download_video(video_url, download_path=None):
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()
        
        if download_path:
            stream.download(output_path=download_path)
        else:
            stream.download()

        print("Video downloaded successfully!")

    except Exception as e:
        print("An error occurred:", e)

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    tqdm_progress_bar.update(percentage_of_completion - tqdm_progress_bar.n)

def main():
    global tqdm_progress_bar
    video_url = input("Enter the YouTube video URL: ")
    download_path = input("Enter the path where you want to save the video (leave blank for default location): ")

    if download_path:
        tqdm_progress_bar = tqdm(total=100, unit='%', unit_scale=True)
        download_video(video_url, download_path)
    else:
        tqdm_progress_bar = tqdm(total=100, unit='%', unit_scale=True)
        download_video(video_url)

if __name__ == "__main__":
    main()
