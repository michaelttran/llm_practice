import assemblyai as aai
import subprocess
import os
from pytubefix import Playlist, YouTube
from pathlib import Path

from data import (
    YOUTUBE_URLS,
    YOUTUBE_PLAYLIST
)

aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")


def fetch_youtube_audios(urls=YOUTUBE_URLS, output_path="downloads/") -> list:
    file_paths = []
    # Create output folder if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    try:
        playlist = Playlist(urls)
    except Exception as e:
        print(f"Failed to initialize playlist: {e}")
        return
    
    print(f"\nDownloading audio from {len(playlist.video_urls)} videos...\n")

    for video_url in playlist.video_urls:
        yt = YouTube(video_url)
        print(f"Processing: {yt.title}")

        # Select the highest bitrate audio-only stream available
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not audio_stream:
            print(f"❌ No audio stream found for: {yt.title}")
            continue

        # Download the audio file
        audio_file_path = audio_stream.download(output_path)
        base, ext = os.path.splitext(audio_file_path)
        mp3_file_path = base + '.mp3'

        # If the file is not already an MP3, convert it using FFmpeg
        if ext.lower() != '.mp3':
            print(f"Converting {yt.title} to MP3...")
            command = [
                'ffmpeg',
                '-y',              # overwrite without asking
                '-i', audio_file_path,
                '-vn',             # no video
                '-ar', '44100',    # set sample rate
                '-ac', '2',        # set number of audio channels
                '-b:a', '192k',    # set audio bitrate
                mp3_file_path
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(f"❌ FFmpeg conversion failed for {yt.title}.\nError: {result.stderr.decode('utf-8')}")
                continue

            # Optionally remove the original file after conversion
            os.remove(audio_file_path)
            print(f"✅ Downloaded and converted: {mp3_file_path}")
        else:
            print(f"✅ Downloaded as MP3: {mp3_file_path}")
        
        file_paths.append(mp3_file_path)
    return file_paths

# TODO: Can also just return the transcriber object
def transcribe(files) -> list:
    print(f"Transcribing with Assembly AI API")
    aapi_transcription_files = []
    config = aai.TranscriptionConfig(speech_models=["universal"])

    for file in files:
        print(f"Transcribing {file}")
        transcript = aai.Transcriber(config=config).transcribe(file)
        # print(f"dir: {dir(transcript)}")
        # print(f"words: {transcript.words}")
        for word in transcript.words:
            print(f"word: {word}")
        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        # print(transcript.text + "\n\n")

        fn = file.split("/")[-1].replace(".mp3", "") # Get the filename because it's at the end of the fp and remove file type
        
        out_dir = Path(f"/Users/michael_tran/git/go_sandbox/aapi_transcriptions")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{fn}-captions.txt"
        out_path.write_text(transcript.text, encoding="utf-8")
        aapi_transcription_files.append(out_path)
    return aapi_transcription_files


def get_video_captions_youtube(urls) -> list:
    playlist = Playlist(urls)
    yt_captions = []

    for video_url in playlist.video_urls:
        yt = YouTube(video_url)

        caption = ( yt.captions.get("en") or yt.captions.get("a.en") or yt.captions.get("en-US"))
        if not caption:
            print(f"couldn't find captions for : {yt.title}")
        
        # Generate SRT text
        srt = caption.generate_srt_captions()

        # Strip SRT timestamps + indexes
        text_lines = []
        for line in srt.splitlines():
            if (
                line.strip().isdigit()
                or "-->" in line
                or not line.strip()
            ):
                continue
            text_lines.append(line)

        plain_text = " ".join(text_lines)
        fp = f"/Users/michael_tran/git/llm_practice/youtube_transcriptions/{yt.title}-captions.txt"
        out_path = Path(fp)
        out_path.write_text(plain_text, encoding="utf-8")
        yt_captions.append(out_path)
    return yt_captions

def get_sources_of_truth(directory="/Users/michael_tran/git/llm_practice/source_of_truth/"):
    print(f"Gathering sources of truth")
    dir_path = Path(directory)
    filenames = [f"{directory}{p.name}" for p in dir_path.iterdir() if p.is_file()]
    return filenames
            
def compare(aapi_transcriptions, yt_transcriptions, sources_of_truth):
    print(f"Comparing")
    print(f"aapi_transcriptions: {aapi_transcriptions} \n || yt_transcriptions: {yt_transcriptions} \n || sources_of_truth: {sources_of_truth} \n")

    for aapi_transcription in aapi_transcriptions:
        print(f"aapi_transcription: {aapi_transcription}")

def main():
    # audio_files = fetch_youtube_audios(urls=YOUTUBE_PLAYLIST)
    # audio_files = ['/Users/michael_tran/git/llm_practice/downloads/Men’s Obsession With Dying In Battle.mp3', '/Users/michael_tran/git/go_sandbox/downloads/How to Get Into 2XKO: Beginner’s Guide to Fighting Games | 2XKO x Core-A Gaming.mp3', '/Users/michael_tran/git/go_sandbox/downloads/21 Savage & Metro Boomin - X ft Future (Official Audio).mp3']
    audio_files = ['/Users/michael_tran/git/llm_practice/downloads/21 Savage & Metro Boomin - X ft Future (Official Audio).mp3']

    # youtube_video_captions = get_video_captions_youtube(YOUTUBE_PLAYLIST)
    youtube_video_captions = ["/Users/michael_tran/git/llm_practice/youtube_transcriptions/21 Savage & Metro Boomin - X ft Future (Official Audio)-captions.txt"]

    aapi_transcription_files =  transcribe(audio_files)
    # aapi_transcription_files = ["/Users/michael_tran/git/llm_practice/aapi_transcriptions/21 Savage & Metro Boomin - X ft Future (Official Audio)-captions.txt"]
    
    # sources_of_truth = get_sources_of_truth()

    # compare(aapi_transcription_files, youtube_video_captions, sources_of_truth)
    


if __name__ == "__main__":
    print(f"Starting Script")
    
    main()

    print(f"Finished Script")