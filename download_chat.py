import pandas as pd
import os
import time
from chat_downloader import ChatDownloader
from tqdm import tqdm


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
def get_chat_in_dataframe(url):
    """

    Args:
        url:

    Returns:

    """
    chat = ChatDownloader().get_chat(url)
    chat_dict = {
        'time_in_seconds': [],
        'message': [],
    }

    for message in tqdm(chat):
        chat_dict['time_in_seconds'].append(message['time_in_seconds'])
        chat_dict['message'].append(message['message'])
    chat_dataframe = pd.DataFrame(chat_dict)

    return chat_dataframe, chat.title


@time_it
def run(urls):
    chats_folder = r'./chats'
    os.makedirs(chats_folder, exist_ok=True)

    for url in urls:
        chat_dataframe, video_title = get_chat_in_dataframe(url)
        video_title = video_title.replace('/', '')
        filepath = os.path.join(chats_folder, video_title)
        chat_dataframe.to_csv(f'{filepath}.csv')


if __name__ == '__main__':
    # urls = ['https://www.youtube.com/watch?v=S8906cHW08g', 'https://www.youtube.com/watch?v=Xp-RgFrGGpg&t']
    urls = ['https://www.youtube.com/watch?v=S8906cHW08g']
    run(urls)
