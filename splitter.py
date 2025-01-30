import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def extract_audio(video_path, output_audio_path):

    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path, codec='pcm_s16le')  # WAV format (PCM 16-bit)

def split_audio(input_audio_path, output_folder, chunk_length_ms=15000):

    os.makedirs(output_folder, exist_ok=True)  # Create folder if not exists
    
    audio = AudioSegment.from_wav(input_audio_path)  # Load audio
    total_length = len(audio)
    
    for i, start in enumerate(range(0, total_length, chunk_length_ms)):
        chunk = audio[start:start + chunk_length_ms]  # Extract 15s chunk
        chunk.export(f"{output_folder}/chunk_{i+1}.wav", format="wav")  # Save chunk

    print(f"Audio split into {i+1} chunks.")



def main():
    video_path = r"C:\NMIMS\Datathon_round2\video.mp4"   # Change to your video file
    output_audio_path = "trial_audio.wav"
    output_folder = "chunk"

    # Extract audio and split it into chunks
    extract_audio(video_path, output_audio_path)
    split_audio(output_audio_path, output_folder)    
if __name__ == "__main__":
    main()
