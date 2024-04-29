import json
import googleapiclient.discovery
import googleapiclient.errors
import re

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "API_KEY"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

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

# Extract video ID from input
video_id = extract_video_id(video_input)
if video_id is None:
    print("Invalid video ID or link. Please try again.")
    exit()

request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=100
)

response = request.execute()

# Create a list to store comments
comments_list = []

# Extract users and comments and append them to the list
for item in response['items']:
    user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    comment_data = {'User': user, 'Comment': comment}
    comments_list.append(comment_data)

# Save comments to a JSON file
output_filename = f"{video_id}_comments.json"
with open(output_filename, 'w', encoding='utf-8') as json_file:
    json.dump(comments_list, json_file, ensure_ascii=False, indent=4)

print(f"Comments scraped and saved to {output_filename}")
