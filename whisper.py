import os
import whisper

def transcribe_audio_chunks(folder_path, output_folder):
    model = whisper.load_model("medium.en")  #model  "small", "medium", or "large"

    
    os.makedirs(output_folder, exist_ok=True)

    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".wav"):
            file_path = os.path.join(folder_path, file)
            print(f"Transcribing {file}...")

            # Perform transcription
            result = model.transcribe(file_path)
            transcript_text = result["text"]

            # Save each transcript separately
            transcript_filename = os.path.splitext(file)[0] + ".txt"
            transcript_path = os.path.join(output_folder, transcript_filename)

            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)

            print(f"Saved: {transcript_filename}")

    print("\nAll transcriptions completed!")

def main():
    folder_path = r"C:\NMIMS\Datathon_round2\output_chunks_aud"
    output_folder = "transcripts"
    transcribe_audio_chunks(folder_path,output_folder)

if __name__ == "__main__":
    main()
