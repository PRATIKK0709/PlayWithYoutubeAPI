import re
import requests

def extract_channel_id(input_str):
    # Check if the input is a channel URL
    channel_id_match = re.match(r'^https?://(?:www\.)?youtube\.com/channel/([a-zA-Z0-9_-]+)', input_str)
    if channel_id_match:
        return channel_id_match.group(1)

    # Check if the input is a channel name
    return input_str

def youtube_channel_id_convert(input_str):
    channel_identifier = extract_channel_id(input_str)

    # YouTube Data API endpoint
    endpoint = "https://www.googleapis.com/youtube/v3/search"

    # Parameters for the request
    params = {
        "key": "",
        "part": "snippet",
        "q": channel_identifier,
        "type": "channel"
    }

    # Sending GET request
    response = requests.get(endpoint, params=params)

    # Processing the response
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and data['items']:
            result = data['items'][0]['id']['channelId']
            print(result)
        else:
            print("No channel found.")
    else:
        print("Error:", response.status_code)

def main():
    input_str = input("Enter the YouTube channel name or link: ")
    youtube_channel_id_convert(input_str)

if __name__ == "__main__":
    main()
