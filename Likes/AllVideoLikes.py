import json
import requests
import time

def fetch_videos(channel_id):
    # Hardcoded YouTube API key
    api_key = 'API-KEY'

    # YouTube Data API endpoint
    endpoint = "https://www.googleapis.com/youtube/v3/search"

    # Parameters for the request
    params = {
        "key": api_key,
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 50,  # Maximum number of videos per request (can be up to 50)
        "order": "date"    # Order by date
    }

    videos = []

    # Fetching videos from the channel
    while True:
        response = requests.get(endpoint, params=params)
        data = response.json()

        # Get channel name
        channel_name = data['items'][0]['snippet']['channelTitle']

        # Process each item in the response
        for item in data['items']:
            # Check if the item represents a video
            if item['id'].get('kind') == 'youtube#video':
                video_id = item['id']['videoId']
                video = {
                    "title": item['snippet']['title'],
                    "likes": get_video_likes(api_key, video_id)
                }
                videos.append(video)

        # Check if there are more pages of results
        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
            # Adding sleep time to avoid hitting API quota limits
            time.sleep(1) # Add 'import time' at the top
        else:
            break

        # Limiting the number of videos to 600
        if len(videos) >= 600:
            break

    return channel_name, videos

def get_video_likes(api_key, video_id):
    # YouTube Data API endpoint for video statistics
    endpoint = "https://www.googleapis.com/youtube/v3/videos"

    # Parameters for the request
    params = {
        "key": api_key,
        "part": "statistics",
        "id": video_id
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if 'items' in data and data['items']:
        return int(data['items'][0]['statistics'].get('likeCount', 0))
    else:
        return 0

def main():
    channel_id = input("Enter the channel ID: ")

    channel_name, videos = fetch_videos(channel_id)

    # Save videos data to a JSON file
    file_name = f"{channel_name}_likes_summary.json"
    with open(file_name, 'w') as json_file:
        json.dump(videos, json_file, indent=4)

    print(f"Videos data saved to '{file_name}'.")

if __name__ == "__main__":
    main()
