import pandas as pd
import time
from chat_downloader import ChatDownloader


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        print(f'{func.__name__} took {time_taken} seconds to complete.')
        return result
    return wrapper


@time_it
def get_all_message_from_chat_in_dataframe(chat):
    chat_dict = {
        'time_in_seconds': [],
        'message': [],
    }
    for message in chat:
        chat_dict['time_in_seconds'].append(message['time_in_seconds'])
        chat_dict['message'].append(message['message'])
    chat_dataframe = pd.DataFrame(chat_dict)
    return chat_dataframe


@time_it
def run():
    url = 'https://www.youtube.com/watch?v=9lPuJIcGdUM'
    # TODO: Comment out for debug purposes. Might need to uncomment in future
    # video_path = download_youtube_video(url)
    chat = ChatDownloader().get_chat(url)
    chat_dataframe = get_all_message_from_chat_in_dataframe(chat)
    # TODO: Create a dictionary with time in minute and number of comments


if __name__ == '__main__':
    run()
