import os
import subprocess
import eyed3

from pytube import YouTube

DOWNLOAD_PATH = "audio"

def load_audio(link: str):
    print(f"[link]: {link}")

    try:
        yt = YouTube(link, use_oauth=True)
        stream = yt.streams.get_by_itag(251)
        try:
            input_file = stream.download(output_path=DOWNLOAD_PATH)
        except:
            print("говно")
            return -1
        output_file = input_file.replace(".webm", ".mp3")

        command = [
            'ffmpeg',
            '-i', input_file,
            '-ab', '192k',
            '-ac', '2',
            '-ar', '44100',
            output_file
        ]
        print(yt.thumbnail_url, "  ", yt.author)
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            return -1
        else:
            print(f'File {input_file} convert to {output_file}')
        audiofile = eyed3.load(output_file)
        audiofile.tag.artist = yt.author
        audiofile.tag.save()
        return output_file
    except:
        print("говно2")
        return -1
    # return stream.download(output_path=DOWNLOAD_PATH)


