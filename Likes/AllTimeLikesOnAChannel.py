import json
import googleapiclient.discovery
import googleapiclient.errors

# API credentials and setup
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "YOUR_API_KEY"

# Create a YouTube API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def get_channel_likes(channel_id):
    try:
        total_likes = 0

        # Request channel uploads playlist ID
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()

        # Check if the response contains any items
        if 'items' in response and response['items']:
            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            # Retrieve all videos from the uploads playlist
            next_page_token = None
            while True:
                playlist_request = youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()

                # Extract video IDs from the playlist response
                video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]

                # Request video statistics for each video
                videos_request = youtube.videos().list(
                    part="statistics",
                    id=",".join(video_ids)
                )
                videos_response = videos_request.execute()

                # Sum up the like counts for all videos
                for video in videos_response['items']:
                    total_likes += int(video['statistics']['likeCount'])

                # Check if there are more pages of videos
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break

        return total_likes
    except googleapiclient.errors.HttpError as e:
        # Handle API errors
        print("An error occurred:", e)
        return None

# Function to load data from JSON file
def load_from_json(file_name):
    try:
        with open(file_name, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {}

# Function to save data to JSON file
def save_to_json(data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Main loop to continuously ask for channel IDs
while True:
    channel_id = input("Enter a YouTube channel ID (or 'q' to quit): ")
    if channel_id.lower() == 'q':
        break
    
    total_likes = get_channel_likes(channel_id)
    if total_likes is not None:
        # Retrieve channel name
        channel_request = youtube.channels().list(
            part="snippet",
            id=channel_id
        )
        channel_response = channel_request.execute()
        channel_name = channel_response['items'][0]['snippet']['title']

        # Display and save data
        print(f"Total likes for the channel '{channel_name}': {total_likes}")
        data = load_from_json('channel_likes.json')
        data[channel_name] = total_likes
        save_to_json(data, 'channel_likes.json')
    else:
        print("Failed to retrieve channel likes.")
