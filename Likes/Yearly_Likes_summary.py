import json
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
import matplotlib.pyplot as plt

# API credentials and setup
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "API KEY"

# Create a YouTube API client
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

def get_channel_likes(channel_id):
    try:
        yearly_likes = {}

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
                    part="statistics,snippet",
                    id=",".join(video_ids)
                )
                videos_response = videos_request.execute()

                # Process each video
                for video in videos_response['items']:
                    # Extract video publish date
                    publish_date = datetime.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                    year = publish_date.year

                    # Extract like count
                    like_count = int(video['statistics'].get('likeCount', 0))

                    # Update yearly likes dictionary
                    if year in yearly_likes:
                        yearly_likes[year] += like_count
                    else:
                        yearly_likes[year] = like_count

                # Check if there are more pages of videos
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break

        return yearly_likes
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

def main():
    # Input channel ID
    channel_id = input("Enter a YouTube channel ID: ")

    # Get yearly likes for the channel
    yearly_likes = get_channel_likes(channel_id)
    if yearly_likes is not None:
        # Retrieve channel name
        channel_request = youtube.channels().list(
            part="snippet",
            id=channel_id
        )
        channel_response = channel_request.execute()
        channel_name = channel_response['items'][0]['snippet']['title']

        # Save data to JSON file
        file_name = f"{channel_name}_yearly_likes.json"
        save_to_json(yearly_likes, file_name)
        print(f"Yearly likes data saved to {file_name}")

        # Display results
        print("Yearly Likes:")
        for year, likes in yearly_likes.items():
            print(f"{year}: {likes}")

        # Sort yearly likes by year
        sorted_yearly_likes = dict(sorted(yearly_likes.items()))

        # Create bar chart
        years = list(sorted_yearly_likes.keys())
        likes = list(sorted_yearly_likes.values())
        plt.bar(years, likes, color='blue')
        plt.xlabel('Year')
        plt.ylabel('Likes')
        plt.title(f'Yearly Likes for Channel: {channel_name}')
        plt.show()
    else:
        print("Failed to retrieve yearly likes.")

if __name__ == "__main__":
    main()
