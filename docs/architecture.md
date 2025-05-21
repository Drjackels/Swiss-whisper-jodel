# swiss-whisper Architecture

## Overview
Swiss-whisper is a web application that allows users to upload MP4 files, extracts audio for transcription using OpenAI's Whisper model, creates an SRT file, and provides an interface to edit and download the transcript.

## Components
- **Frontend:**  
  Provides an upload page and an editing interface.
- **Backend:**  
  A Flask application that handles:
  - File uploads and storage (ephemeral in the uploads folder)
  - Audio extraction via ffmpeg
  - Transcription via the Whisper model
  - SRT generation from transcription segments
  - Routes to edit and download the final transcript
- **Storage:**  
  Temporary storage is managed in the `uploads/` folder.

## Future Enhancements
- Asynchronous transcription processing for longer videos.
- User authentication and persistent storage of past transcripts.
- Containerization using Docker for deployment on cloud services.
