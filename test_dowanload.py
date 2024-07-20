import yt_dlp

def download_audio_with_yt_dlp(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'video')
            ydl.download([video_url])
    except:
        return -1
    audio_filename = f'audio/{video_title}.mp3'
    return audio_filename
    #.webm.part
if __name__ == "__main__":
    url = "https://youtu.be/d4uA3t9AOUw?si=Cs1MZCqlTRm4x5Fi"
    download_audio_with_yt_dlp(url)
