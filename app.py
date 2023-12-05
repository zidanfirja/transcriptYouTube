from flask import Flask
from flask_restful import Resource, Api, reqparse
from pytube import YouTube, extract
import whisper
import re
import googleapiclient.discovery

app = Flask(__name__)
api = Api(app)

# link, filename, video_id, transcript


parse = reqparse.RequestParser()
parse.add_argument("link", required=True)

class Transcript(Resource):
    def __init__(self):
        self.pattern_url = re.compile(
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        self.data = {}
        self.API_KEY = "AIzaSyClq5D1GB7EzUewH9j0ChZcGSSAS8Ls6vA"

    def create_and_open_txt(self, text, filename):
        with open(filename, "w") as file:
            file.write(text)

    def url_validation(self, url):
        video_id = extract.video_id(url)
        self.data.update({'link': url, 'id' : video_id})
        return bool(self.pattern_url.match(url))
    
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

    def download_audio_stream(self, url):
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_path = "YoutubeAudios"
        
        filename = f"audio_{self.data['id']}.mp3"
        audio_stream.download(output_path=output_path, filename=filename)
        print(f"Audio downloaded successfully!")

        self.data.update({'filename': filename, 'output_path': output_path})

    def transcript_audio(self):
        model = whisper.load_model("base")
        audio_path = f"YoutubeAudios/audio_{self.data['id']}.mp3"
        result = model.transcribe(audio_path, fp16=False)
        transcribed_text = result["text"]
        print("Transcript success!")
        self.data['transcribed_text'] = transcribed_text
        self.create_and_open_txt(transcribed_text, f"transcript_{self.data['id']}.txt")
        print("Data store success!")

    def post(self):
        args = parse.parse_args()
        self.data['link'] = args['link']
        
        try :
            if not self.url_validation(self.data['link']):
                return {"error": "Enter the correct YouTube link"}, 400
        except Exception as e:
            return {'error' : 'An error occurred, please check the link you used'}

        if not self.is_video_available(self.API_KEY, self.data['id']):
            return {"error": "video doesnt exist anymore"}, 400

        try:
            self.download_audio_stream(self.data['link'])
            self.transcript_audio()
            return {'status': 'Success', 'body': self.data}, 200
        except Exception as e:
            return str(e), 400


api.add_resource(Transcript, '/trans')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
