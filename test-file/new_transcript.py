from youtube_transcript_api import YouTubeTranscriptApi
import pytube

def transcribe_youtube_video(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en','id'])
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# Ganti 'YOUR_YOUTUBE_VIDEO_ID' dengan ID video YouTube yang ingin Anda transkripsi
video_id = '6twPjWO2fiM'

transcription = transcribe_youtube_video(video_id)

print("Hasil Transkripsi:")
print(transcription)

# https://youtu.be/6twPjWO2fiM?si=2XHPiTPv7jIoFY-L
# url1='http://youtu.be/SA2iWivDJiE'
# url2='http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu'
# url3='http://www.youtube.com/embed/SA2iWivDJiE'
# url4='http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US'
# url5='https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6'
# url6='youtube.com/watch?v=_lOT2p_FCvA'
# url7='youtu.be/watch?v=_lOT2p_FCvA'
# url8='https://www.youtube.com/watch?time_continue=9&v=n0g-Y0oo5Qs&feature=emb_logo'

# urls=[url1,url2,url3,url4,url5,url6,url7,url8]

# #Get youtube id
# from pytube import extract
# for url in urls:
#     id=extract.video_id(url)
#     print(id)