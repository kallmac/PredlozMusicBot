from youtube_search import YoutubeSearch
import requests

def is_video_on_youtube_music(video_id):
    url = f"https://music.youtube.com/youtubei/v1/music/get_watch_playlist?videoId={video_id}"
    response = requests.get(url)
    return response.status_code == 200

def search_youtube_track(track_name):
    results = YoutubeSearch(track_name, max_results=5).to_dict()

    videos = []
    for result in results:
        video_id = result['id']
        if is_video_on_youtube_music(video_id):
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(video_link)

    return tuple(videos)

if __name__ == "__main__":
    track_name = input("Введите название трека: ")
    search_results = search_youtube_track(track_name)
    print(search_results)

    print(is_video_on_youtube_music("PieMkyGnS3MfBwzp"))