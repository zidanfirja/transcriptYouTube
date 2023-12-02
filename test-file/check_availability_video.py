import googleapiclient.discovery

def is_video_available(api_key, video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

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

# Replace with your API key and video ID
api_key = "AIzaSyClq5D1GB7EzUewH9j0ChZcGSSAS8Ls6vA"
video_id = "YZ5tOe7y9x4"

# Check video availability
availability = is_video_available(api_key, video_id)
print(f"Video Availability: {availability}")