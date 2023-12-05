from flask import Flask
from flask_restful import Resource, Api, reqparse
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
import re
import googleapiclient.discovery


app = Flask(__name__)
api = Api(app)

# Constants
PATTERN_URL = (
    r'(https?://)?(www\.)?'
    '(youtube|youtu|youtube-nocookie)\.(com|be)/'
    '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
)


API_KEY = "AIzaSyClq5D1GB7EzUewH9j0ChZcGSSAS8Ls6vA"


class Transcript(Resource):
    def __init__(self):
        self.data = {}

    def url_path_validation(self, url):
        pattern_url_match = re.match(PATTERN_URL, url)
        return bool(pattern_url_match)
    
    def is_video_available(self, API_KEY, video_id):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

        # Make API request to get video details
        request = youtube.videos().list(part="status", id=video_id)
        response = request.execute()

        # Check if the response contains the video details
        items = response.get("items", [])
        if items:
            status = items[0]["status"]
            upload_status = status.get("uploadStatus")
            
            # Check if video is available
            return upload_status == "processed"
        else:
            return False

    def create_and_open_txt(self, text, filename):
        with open(filename, "w") as file:
            file.write(text)

    def transcribe_youtube_video(self, url):
        
        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.data['id'], languages=['en','id'])
            text = ' '.join([entry['text'] for entry in transcript])
            return text
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    # def download_audio_stream(self, url):
    #     yt = YouTube(url)
    #     audio_stream = yt.streams.filter(only_audio=True).first()
    #     id = extract.video_id(url)
    #     filename = f"audio_{id}.mp3"
    #     audio_stream.download(output_path=OUTPUT_PATH, filename=filename)
    #     print("Audio downloaded successfully!")
    #     self.data.update({'link': url, 'filename': filename, 'id': id, 'output_path': OUTPUT_PATH})

    # def transcript_audio(self):
    #     model = whisper.load_model("base")
    #     audio_path = f"{OUTPUT_PATH}/audio_{self.data['id']}.mp3"
    #     result = model.transcribe(audio_path, fp16=False)
    #     transcribed_text = result["text"]
    #     print("Transcription successful!")
    #     self.data['transcribed_text'] = transcribed_text
    #     transcript_filename = f"transcript_{self.data['id']}.txt"
    #     self.create_and_open_txt(transcribed_text, transcript_filename)
    #     print("Data stored successfully!")

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("link", required=True)
        args = parse.parse_args()
        self.data['link'] = args['link']

        if not self.url_path_validation(self.data['link']):
            return {"error": "Enter the correct YouTube link"}, 400
        
        video_id = extract.video_id(self.data['link'])
        self.data['id'] = video_id

        if not self.is_video_available(API_KEY, self.data['id']):
            return {"error": "video doesnt exist anymore"}, 400

        try:
            transcription = self.transcribe_youtube_video(self.data['link'])
            self.data['transcription'] = transcription
            
            return {'status': 'Success', 'body': self.data}, 200
        except FileNotFoundError:
            return {"error": "Audio file not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400


api.add_resource(Transcript, '/trans')

if __name__ == '__main__':
    app.run(debug=True)
