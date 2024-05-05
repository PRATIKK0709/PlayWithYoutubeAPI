import json
import pytchat


def fetch_and_save_live_chat(video_id, output_file):
    chat = pytchat.create(video_id=video_id)
    
    with open(output_file, 'a') as json_file:
        while chat.is_alive():
            for c in chat.get().sync_items():
                message_data = {
                    'datetime': str(c.datetime),
                    'username': c.author.name,
                    'message': c.message
                }
                json.dump(message_data, json_file)
                json_file.write('\n')
                json_file.flush()  
                print(f"{c.datetime} [{c.author.name}]- {c.message}")


if __name__ == "__main__":
    video_id = input("Enter the ID of the live stream video: ")  
    output_file = 'live_chat_messages.json'

    fetch_and_save_live_chat(video_id, output_file)
