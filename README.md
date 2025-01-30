 Audio Splitting and Transcription using Whisper

 Overview
This project splits an audio file into smaller chunks and then transcribes each chunk using OpenAI's Whisper model. The transcripts are saved as text files for further processing.

 Prerequisites
Ensure you have the following installed before running the code:

- Python 3.8 or later
- FFmpeg (for audio processing)
- Required Python libraries:
  ```bash
  pip install ffmpeg-python openai-whisper torch
  ```

 Steps

 1. Audio Splitting
The audio file is split into smaller chunks using FFmpeg. This ensures that Whisper processes manageable portions, improving transcription accuracy and efficiency.

Code:
```python
import os
import ffmpeg

def split_audio(input_audio, output_folder, chunk_duration=30):
    os.makedirs(output_folder, exist_ok=True)
    
    command = (
        f"ffmpeg -i {input_audio} -f segment -segment_time {chunk_duration} "
        f"-c copy {output_folder}/chunk_%03d.wav"
    )
    os.system(command)
    print("Audio split successfully.")
```

Usage:
```python
split_audio("input_audio.wav", "output_chunks")
```

 2. Transcription using Whisper
Each split audio chunk is transcribed using the Whisper model.

Code:
```python
import whisper
import os

def transcribe_audio_chunks(input_folder, output_folder):
    model = whisper.load_model("base")   Load Whisper model
    os.makedirs(output_folder, exist_ok=True)
    
    for file in sorted(os.listdir(input_folder)):
        if file.endswith(".wav"):
            file_path = os.path.join(input_folder, file)
            result = model.transcribe(file_path)
            
            output_text_file = os.path.join(output_folder, f"{file}.txt")
            with open(output_text_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
    
    print("Transcription completed.")
```

Usage:
```python
transcribe_audio_chunks("output_chunks", "transcripts")
```

 File Structure
```
project_folder/
│── input_audio.wav
│── output_chunks/
│   │── chunk_000.wav
│   │── chunk_001.wav
│   │── ...
│── transcripts/
│   │── chunk_000.wav.txt
│   │── chunk_001.wav.txt
│── splitter.py
│── whisper_transcribe.py
│── README.md
```

 Notes
- Ensure `FFmpeg` is installed and accessible in your system's path.
- Whisper's accuracy depends on the model size (`base`, `small`, `medium`, `large`). Choose based on your hardware and needs.

 Credits
- OpenAI Whisper: https://github.com/openai/whisper
- FFmpeg: https://ffmpeg.org/

 License
This project is open-source under the MIT License.

