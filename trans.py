from youtube_transcript_api import YouTubeTranscriptApi
# https://www.youtube.com/watch?v=YZ5tOe7y9x4       --> ini dari search bar yt
# https://youtu.be/YZ5tOe7y9x4?si=Am-7l7sEyg5crxXP  --> ini dari share video yt

data = YouTubeTranscriptApi.get_transcript("YZ5tOe7y9x4")
# print(data)


transcript = ''
for value in data:
    for key, item in value.items():
        if key == 'text':
            transcript += item

l = transcript.splitlines()
final_tra = " ".join(l)

print(final_tra)