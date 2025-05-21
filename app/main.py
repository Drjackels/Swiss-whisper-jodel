import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
from flask import Flask, render_template, request, redirect, url_for, send_file
import whisper
from app.srt_generator import generate_srt
from app.ffmpeg_utils import extract_audio

print("DEBUG: Entering main.py...")

app = Flask(__name__)
print("DEBUG: Created Flask app.")

# Load the Whisper model (choose your desired model variant; e.g., "base")
print("DEBUG: Loading Whisper model...")
model = whisper.load_model("tiny")
print("DEBUG: Whisper model loaded.")

# Define the uploads folder (ensure it exists)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
print("DEBUG: Uploads folder is set at:", UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def index():
    # Render the upload page template. Ensure that app/templates/index.html exists.
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return "No file provided", 400

    mp4_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(mp4_path)
    print("DEBUG: Saved MP4 file to", mp4_path)

    # Extract audio from the MP4 file
    audio_path = os.path.join(UPLOAD_FOLDER, "audio.wav")
    extract_audio(mp4_path, audio_path)
    print("DEBUG: Extracted audio to", audio_path)

    # Transcribe the audio using Whisper
    result = model.transcribe(audio_path)
    print("DEBUG: Transcription complete.")

    # Generate SRT content from the transcription result
    srt_content = generate_srt(result)
    print("DEBUG: Generated SRT content.")

    # Save the generated SRT file
    srt_path = os.path.join(UPLOAD_FOLDER, "transcript.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print("DEBUG: Saved SRT file to", srt_path)

    # Redirect to the edit page for user corrections
    return redirect(url_for('edit'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    srt_path = os.path.join(UPLOAD_FOLDER, "transcript.srt")
    if request.method == 'POST':
        edited_text = request.form.get("transcript")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(edited_text)
        print("DEBUG: Transcript updated via edit page.")
        return redirect(url_for('download'))
    else:
        with open(srt_path, "r", encoding="utf-8") as f:
            srt_text = f.read()
        # Render the edit template, passing the SRT content for the user to correct.
        return render_template("edit.html", transcript=srt_text)

@app.route('/download', methods=['GET'])
def download():
    srt_path = os.path.join(UPLOAD_FOLDER, "transcript.srt")
    print("DEBUG: Serving SRT file for download from", srt_path)
    return send_file(srt_path, as_attachment=True, download_name="transcript.srt")

if __name__ == "__main__":
    print("DEBUG: About to run app...")
    app.run(host="0.0.0.0", port=8080, debug=True)


