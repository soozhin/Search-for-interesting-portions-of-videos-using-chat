import os.path

import pandas as pd
import time
import matplotlib.pyplot as plt
import japanize_matplotlib
from glob import glob
from tqdm import tqdm
from chat_downloader import ChatDownloader
from pathlib import Path


def time_it(func):
    """A decorator that inform users about the start of the function and the time taken to complete the function

    Args:
        func: The function to be called

    Returns:
        wrapper function
    """

    def wrapper(*args, **kwargs):
        print(f'Started [{func.__name__}]...')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        print(f'[{func.__name__}] took [{time_taken:.2f}] seconds to complete.')
        return result

    return wrapper


@time_it
def get_all_message_from_chat_in_dataframe(chat):
    """Return time_in_seconds and message from chat in dataframe form

    Args:
        chat: A chat object that includes time_in_seconds and message

    Returns:
        time_in_seconds and message from chat in dataframe form
    """
    chat_dict = {
        'time_in_seconds': [],
        'message': [],
    }
    for message in tqdm(chat):
        chat_dict['time_in_seconds'].append(message['time_in_seconds'])
        chat_dict['message'].append(message['message'])
    chat_dataframe = pd.DataFrame(chat_dict)
    return chat_dataframe


@time_it
def get_number_of_comments_per_minute(chat_dataframe):
    """Return a dataframe of number of comments per minute

    Args:
        chat_dataframe: A panda dataframe that contains time_in_seconds and message

    Returns:
        A dataframe of number of comments per minute
    """
    number_of_comments_per_minute = {
        'time_in_seconds': [],
        'number_of_comments': [],
    }
    current_time_in_seconds = chat_dataframe['time_in_seconds'][0]
    count = 0

    for index in range(len(chat_dataframe)):
        if chat_dataframe['time_in_seconds'][index] > (current_time_in_seconds + 60):
            number_of_comments_per_minute['time_in_seconds'].append(current_time_in_seconds)
            number_of_comments_per_minute['number_of_comments'].append(count)
            current_time_in_seconds = chat_dataframe['time_in_seconds'][index]
            count = 0
        else:
            count += 1

    if count > 0:
        number_of_comments_per_minute['time_in_seconds'].append(current_time_in_seconds)
        number_of_comments_per_minute['number_of_comments'].append(count)

    return pd.DataFrame(number_of_comments_per_minute)


@time_it
def run():
    # TODO: Currently only testing out on 1 youtube video. Might need to expand this to be able to handle multiple videos from miltiple streamers
    url = 'https://www.youtube.com/watch?v=Xp-RgFrGGpg&t'
    # TODO: Comment out for debug purposes. Might need to uncomment in future
    # video_path = download_youtube_video(url)

    # Download the chat from the stream
    # TODO: Do not need to download everytime anymore because I implemented this in another python script.
    # chat = ChatDownloader().get_chat(url)
    # chat_dataframe = get_all_message_from_chat_in_dataframe(chat)

    chat_filepath = r'./chats/100万人ありがとよ！しぐれうい丸わかりスペシャル.csv'
    video_title = Path(chat_filepath).stem
    chat_dataframe = pd.read_csv(chat_filepath)

    # Create a dataframe with time in minute and number of comments
    number_of_comments_per_minute = get_number_of_comments_per_minute(chat_dataframe)
    number_of_comments_per_minute['number_of_comments'].plot()
    plt.title(f'Graph of number of comments per minute for [{video_title}]')
    plot_filepath = rf'Graph_of_number_of_comments_per_minute_for_{video_title}'
    plt.savefig(plot_filepath)

if __name__ == '__main__':
    run()
