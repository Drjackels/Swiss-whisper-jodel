def generate_srt(transcription_result: dict) -> str:
    """
    Convert Whisper transcription result to SRT format.
    Assumes transcription_result contains a 'segments' key.
    """
    segments = transcription_result.get("segments", [])
    srt_output = ""
    for index, segment in enumerate(segments, start=1):
        start_time = format_srt_time(segment["start"])
        end_time = format_srt_time(segment["end"])
        text = segment["text"].strip()
        srt_output += f"{index}\n{start_time} --> {end_time}\n{text}\n\n"
    return srt_output

def format_srt_time(seconds: float) -> str:
    """
    Convert seconds to SRT time format (HH:MM:SS,mmm).
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
