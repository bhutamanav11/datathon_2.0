import os
import librosa
import webrtcvad
import numpy as np
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import nltk
from moviepy.editor import VideoFileClip

# Download necessary NLTK data
nltk.download('punkt')

# Function to extract audio from video
def extract_audio_from_video(video_path, output_audio_path="output_audio.wav"):
    """
    Extract audio from a video file and save it as a .wav file.
    """
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path)
    return output_audio_path

# Step 1: Load the audio from the video
def load_audio(file_path, target_sr=16000):
    """
    Load audio using librosa and resample to 16kHz (required by Vosk).
    """
    audio, sr = librosa.load(file_path, sr=target_sr)
    return audio, sr

# Step 2: Transcribe audio with Vosk
def transcribe_audio(audio_path, vosk_model_path="C:/NMIMS/Datathon_round2/vosk-model-small-en-us-0.15"):
    """
    Transcribe audio using Vosk model.
    """
    model = Model(vosk_model_path)
    recognizer = KaldiRecognizer(model, 16000)

    # Read the audio file
    audio = AudioSegment.from_wav(audio_path)
    audio_samples = np.array(audio.get_array_of_samples())

    # Start recognizing
    transcript = ""
    for i in range(0, len(audio_samples), 4000):  # Process in chunks
        audio_chunk = audio_samples[i:i+4000]
        if recognizer.AcceptWaveform(audio_chunk.tobytes()):
            result = recognizer.Result()
            transcript += result

    # Return the complete transcript
    return transcript

# Step 3: Perform Voice Activity Detection (VAD) using WebRTC
def apply_vad(audio, sr, frame_duration_ms=30):
    """
    Use WebRTC VAD to detect speech segments.
    """
    vad = webrtcvad.Vad()
    vad.set_mode(3)  # 0-3 (3 is the most aggressive for detecting speech)

    frame_length = int(frame_duration_ms / 1000 * sr)  # Frame length in samples
    speech_segments = []

    # Convert audio to 16-bit PCM format
    audio = (audio * 32768).astype(np.int16)

    # Process each frame
    for i in range(0, len(audio), frame_length):
        frame = audio[i:i + frame_length]
        if len(frame) < frame_length:
            break  # Skip incomplete frames
        # Check if the frame contains speech
        is_speech = vad.is_speech(frame.tobytes(), sr)
        speech_segments.append((i / sr, (i + frame_length) / sr, is_speech))

    return speech_segments

import re

# Step 4: Perform Semantic Segmentation using Regular Expressions
def segment_text(transcript):
    """
    Use regular expressions for sentence segmentation.
    """
    # Split text on sentence-ending punctuation followed by a space or end of string
    sentences = re.split(r'(?<=[.!?]) +', transcript.strip())
    return sentences

# Step 5: Combine VAD and Semantic Segmentation for Chunking
def create_chunks(transcription_result, speech_segments, max_chunk_duration=15):
    """
    Combine VAD and semantic segmentation to generate chunks.
    """
    chunks = []
    current_chunk = []
    current_start_time = None
    current_duration = 0

    # Iterate through speech segments and match them with transcript sentences
    for segment in speech_segments:
        start_time, end_time, is_speech = segment
        if is_speech:
            duration = end_time - start_time
            if current_duration + duration <= max_chunk_duration:
                if current_start_time is None:
                    current_start_time = start_time
                current_duration += duration
            else:
                chunks.append((current_start_time, start_time))  # Save the chunk
                current_start_time = start_time
                current_duration = duration

    # Add the last chunk if it exists
    if current_start_time is not None:
        chunks.append((current_start_time, current_start_time + current_duration))

    return chunks


# Step 6: Save Chunks
import soundfile as sf 

def save_chunks(chunks, audio, sr, output_dir="output_chunks"):
    """
    Save each chunk as a separate audio file.
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, (start_time, end_time) in enumerate(chunks):
        # Convert start and end times to sample indices
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        chunk_audio = audio[start_sample:end_sample]

        # Save the audio chunk using soundfile
        output_path = os.path.join(output_dir, f"chunk_{i + 1}.wav")
        sf.write(output_path, chunk_audio, sr)
        print(f"Saved: {output_path}")



# Full Pipeline Execution
# Main pipeline
def main():
    # File paths
    video_file = r"C:\NMIMS\Datathon_round2\video.mp4"  # Update with your local video file path
    audio_file = "output_audio.wav"  # Temporary audio file extracted from video

    # Step 1: Extract audio from video
    print("Extracting audio from video...")
    audio_file = extract_audio_from_video(video_file, audio_file)
    print(f"Audio extracted to: {audio_file}")

    # Step 2: Load the audio
    print("Loading audio...")
    audio, sr = load_audio(audio_file)

    # Step 3: Transcribe audio
    print("Transcribing audio...")
    transcription = transcribe_audio(audio_file)
    print("Transcription completed.")

    # Step 4: Detect voice activity
    print("Applying Voice Activity Detection (VAD)...")
    vad_segments = apply_vad(audio, sr)

    # Step 5: Segment transcript
    print("Segmenting transcript...")
    sentences = segment_text(transcription)

    # Step 6: Generate chunks
    print("Creating chunks...")
    chunks = create_chunks(transcription, vad_segments)

    # Step 7: Save chunks
    print("Saving chunks...")
    save_chunks(chunks, audio, sr)
    print("All chunks saved successfully!")
# Run the program
if __name__ == "__main__":
    main()
