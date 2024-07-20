from youtube_search import YoutubeSearch
import yt_dlp
import eyed3
import subprocess


def convert_webp_to_png(input_file):
    output_file = input_file.split('.')[0] + ".png"
    command = f"ffmpeg -i {input_file} {output_file}"
    subprocess.run(command, shell=True)

def add_cover_to_audio(audio_file, cover_image):
    audio = eyed3.load(audio_file)
    if audio.tag is None:
        audio.initTag()

    with open(cover_image, "rb") as image_file:
        image_data = image_file.read()

    audio.tag.images.set(3, image_data, "image/png")
    audio.tag.save()

def refactor_title(title: str):
    words = title.split()
    for i in range(len(words)):
        if "(" in words[i] and ")" in words[i]:
            words.pop(i)
    # ХЗ, Надо ли это
    """ 
    if '-' in words:
        deleted = ''
        while deleted != '-':
            deleted = words.pop(0)
        result = ' '.join(words)
        if len(result) <= 21:
            return result
    """
    while sum(map(len, words)) + len(words) - 1 > 18:
        words.pop()
    return ' '.join(words) + "..."


def search_youtube_track(track_name):
    results = YoutubeSearch(track_name, max_results=10).to_dict()
    videos = {}
    for result in results:
        title_duration = refactor_title(result['title'])
        video_id = result['id']
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        videos[title_duration] = video_link

    return videos


def download_audio_with_yt_dlp(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'writethumbnail': True,
        'outtmpl': 'audio/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'video')
            ydl.download([video_url])
    except:
        return -1
    convert_webp_to_png(f'audio/{video_title}.webp')
    img_filename = f'audio/{video_title}.png'
    audio_filename = f'audio/{video_title}.mp3'
    add_cover_to_audio(audio_filename, img_filename)
    return audio_filename


if __name__ == '__main__':
    print(download_audio_with_yt_dlp(input("ссылка: ")))