from pytube import YouTube,extract
import whisper
# from youtube_transcript_api import YouTubeTranscriptApi

# https://www.youtube.com/watch?v=YZ5tOe7y9x4       --> ini dari search bar yt
# https://youtu.be/YZ5tOe7y9x4?si=Am-7l7sEyg5crxXP  --> ini dari share video yt


# Function to create and open a txt file
def create_and_open_txt(text, filename):
    # Create and write the text to a txt file
    with open(filename, "w") as file:
        file.write(text)
    # startfile(filename)


# Ask user for the YouTube video URL
url = input("Enter the YouTube video URL: ")

# Create a YouTube object from the URL
yt = YouTube(url)

# Get the audio stream
audio_stream = yt.streams.filter(only_audio=True).first()

# Download the audio stream
output_path = "YoutubeAudios"
id = extract.video_id(url)
filename = f"audio_{id}.mp3"
print(filename)

# coba cari transcript indonesia
# transcript_list = YouTubeTranscriptApi.get_transcript(id)
# transcript = transcript_list.find_transcript(['id', 'en'])
# print(transcript)
# for x, tr in enumerate(transcript):
#   print(tr.language_code)

audio_stream.download(output_path=output_path, filename=filename)

print(f"Audio downloaded to {output_path}/{filename}")

# Load the base model and transcribe the audio
model = whisper.load_model("base")
result = model.transcribe("YoutubeAudios/audio.mp3", fp16=False)
transcribed_text = result["text"]
# print(transcribed_text)

# # Create and open a txt file with the text
create_and_open_txt(transcribed_text, f"transcript_{id}.txt")
