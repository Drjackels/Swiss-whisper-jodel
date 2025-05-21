import subprocess

def extract_audio(mp4_path: str, audio_path: str) -> None:
    """
    Extract audio from an MP4 file and save it as a WAV file.
    Requires ffmpeg to be installed on the system.
    """
    command = [
        "ffmpeg",
        "-y",
        "-i", mp4_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]
    subprocess.run(command, check=True)
