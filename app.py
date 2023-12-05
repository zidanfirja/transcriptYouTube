from flask import Flask
from flask_restful import Resource, Api, reqparse
from pytube import YouTube,extract
import whisper
import re

app = Flask(__name__)
api = Api(app)

# link, filename, video_id, transcript
data = {}

parse = reqparse.RequestParser()
parse.add_argument("link", required=True)

class Hello(Resource):
    def get(self):
        return {'body' : 'hallo'}
    
class Transcript(Resource):
    def url_validation(self, url):
        pattern_url = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        pattern_url_match = re.match(pattern_url, url)
        if pattern_url_match:
            return True
        return False

    def create_and_open_txt(self,text, filename):
        with open(filename, "w") as file:
            file.write(text)

    def download_audio_stream(self, url):
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_path = "YoutubeAudios"
        id = extract.video_id(url)
        filename = f"audio_{id}.mp3"
        audio_stream.download(output_path=output_path, filename=filename)
        print(f"Audio downloaded success!")

        data.update({'link' : url, 'filename' : filename, 'id': id, 'output_path' : output_path})

    def transcript_audio(self):
        model = whisper.load_model("base")
        result = model.transcribe(f"YoutubeAudios/audio_{data['id']}.mp3", fp16=False)
        transcribed_text = result["text"]
        print(f"Transcript success!")
        data['transcribed_text'] = transcribed_text
        self.create_and_open_txt(transcribed_text, f"transcript_{data['id']}.txt")
        print(f"data store success!")

    def post(self):
        args = parse.parse_args()
        data['link'] = args['link']
    
        if not self.url_validation(data['link']):
            return {"error": "Enter the correct YouTube link"}, 400

        try:    
            self.download_audio_stream(data['link'])
            self.transcript_audio()
            return {'status' : 'Success','body' : data}, 200
        except Exception as e:
            return e, 400
        
api.add_resource(Hello, '/')
api.add_resource(Transcript, '/trans')

if __name__ == '__main__':
    app.run(debug=True, port=5050)