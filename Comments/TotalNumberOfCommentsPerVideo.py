import os
import json
import googleapiclient.discovery

# Initialize the YouTube Data API client
DEVELOPER_KEY = "API_KEY"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=DEVELOPER_KEY)

def get_channel_name(channel_id):
    try:
        channel_response = youtube.channels().list(
            part="snippet",
            id=channel_id
        ).execute()

        channel_name = channel_response["items"][0]["snippet"]["title"]
        return channel_name

    except googleapiclient.errors.HttpError as e:
        print("An error occurred:", e)
        return None

def get_video_info(channel_id):
    video_info_list = []
    
    try:
        # Fetch videos uploaded by the channel
        next_page_token = None
        while True:
            search_response = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                type="video",
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            video_ids = [item["id"]["videoId"] for item in search_response["items"]]
            videos_response = youtube.videos().list(
                part="snippet,statistics",
                id=",".join(video_ids)
            ).execute()
            
            # Extract title and total number of comments for each video
            for video in videos_response["items"]:
                video_info = {
                    "title": video["snippet"]["title"],
                    "total_comments": int(video["statistics"].get("commentCount", 0))
                }
                video_info_list.append(video_info)
            
            next_page_token = search_response.get("nextPageToken")
            if not next_page_token:
                break

    except googleapiclient.errors.HttpError as e:
        print("An error occurred:", e)
    
    return video_info_list

if __name__ == "__main__":
    # Ask user for channel ID
    channel_id = input("Enter the channel ID: ")
    channel_name = get_channel_name(channel_id)

    if channel_name:
        video_info_list = get_video_info(channel_id)
        
        # Save video info to a JSON file
        output_file = f"{channel_name}_total_comments.json"
        with open(output_file, "w") as json_file:
            json.dump(video_info_list, json_file, indent=4)

        print(f"Video information has been saved to '{output_file}'.")
