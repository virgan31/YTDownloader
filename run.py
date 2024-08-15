from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from tqdm import tqdm
import os

def search_youtube(query, max_results=5):
    search = VideosSearch(query, limit=max_results)
    results = search.result()['result']
    
    print("\nSearch Results:")
    for index, video in enumerate(results, start=1):
        print(f"{index}. {video['title']} (Duration: {video['duration']})")
        print(f"   Link: {video['link']}\n")
    
    return results

def download_video(video_url, download_audio=False, download_path="."):
    try:
        ydl_opts = {
            'format': 'bestaudio/best' if download_audio else 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if download_audio else [],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print("Download completed!")
            
    except Exception as e:
        print(f"Error: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        if not progress_hook.pbar:
            total = d.get('total_bytes', 0)
            progress_hook.pbar = tqdm(total=total, unit='B', unit_scale=True, desc="Downloading")
        
        progress_hook.pbar.update(d['downloaded_bytes'] - progress_hook.pbar.n)
    
    elif d['status'] == 'finished':
        if progress_hook.pbar:
            progress_hook.pbar.close()
        print("Done downloading, now converting...")
progress_hook.pbar = None

def main():
    query = input("Enter search query: ")
    search_results = search_youtube(query)
    
    try:
        choice = int(input("Enter the number of the video you want to download: "))
        if 1 <= choice <= len(search_results):
            selected_video = search_results[choice - 1]
            print(f"\nSelected: {selected_video['title']}")
            
            download_type = input("Download video or audio-only? (v/a): ").strip().lower()
            download_audio = (download_type == 'a')
            
            # Folder selection
            folder_choice = input("Choose folder: Music, Video, or Other (m/v/o): ").strip().lower()
            if folder_choice == 'm':
                download_path = os.path.join(os.getcwd(), 'Music')
            elif folder_choice == 'v':
                download_path = os.path.join(os.getcwd(), 'Video')
            else:
                download_path = os.path.join(os.getcwd(), 'Other')
            
            # Create the folder if it doesn't exist
            os.makedirs(download_path, exist_ok=True)
            
            print(f"Downloading {'audio' if download_audio else 'video'} to {download_path}...")
            download_video(selected_video['link'], download_audio, download_path)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
