import json
from googleapiclient.discovery import build
import re

# Set up YouTube API service
api_key = "YOUR_API_KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to retrieve user information
def get_user_info(channel_id):
    user_info = youtube.channels().list(
        part="snippet",
        id=channel_id
    ).execute()
    if user_info["items"]:
        return user_info["items"][0]["snippet"]["title"]
    else:
        return "Unknown User"

# Function to get video title
def get_video_title(video_id):
    video_info = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    if video_info["items"]:
        return video_info["items"][0]["snippet"]["title"]
    else:
        return "Unknown Title"

# Function to extract video ID from video URL
def extract_video_id(video_input):
    # Regular expression to extract video ID from URL
    regex = r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=|(?:(?:.be\/)|(?:watch\/)))([a-zA-Z0-9_-]{11})'
    match = re.search(regex, video_input)
    if match:
        return match.group(1)
    else:
        return None

# Prompt user for video ID or video link
video_input = input("Enter the video ID or video link: ")
video_id = extract_video_id(video_input)
if video_id is None:
    # If input is not a valid video ID or link, assume it's a video ID directly
    video_id = video_input

# Retrieve comments for the specified video
comments = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=100,  # Adjust as needed
    order="relevance",  # You can also sort by time if you prefer
).execute()

# Sort comments by like count
sorted_comments = sorted(comments["items"], key=lambda x: int(x["snippet"]["topLevelComment"]["snippet"]["likeCount"]), reverse=True)

# Get most liked comments
most_liked_comments = sorted_comments[:10]  # Select top 10 most liked comments

# Get video title
video_title = get_video_title(video_id)

# Create a list to store comments data
comments_data = []

# Prepare comments data
for comment in most_liked_comments:
    comment_snippet = comment["snippet"]["topLevelComment"]["snippet"]
    username = get_user_info(comment_snippet["authorChannelId"]["value"])
    comment_data = {
        "username": username,
        "comment": comment_snippet["textDisplay"],
        "likes": comment_snippet["likeCount"]
    }
    comments_data.append(comment_data)

# Save comments data to a JSON file
output_filename = f"{video_title}_most_liked_comments.json"
with open(output_filename, "w") as file:
    json.dump(comments_data, file, indent=4)

print(f"Most liked comments data saved to '{output_filename}'.")
