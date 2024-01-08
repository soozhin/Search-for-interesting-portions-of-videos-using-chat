import os
import pandas
import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import japanize_matplotlib
import glob
from tqdm import tqdm
from datetime import timedelta
from pathlib import Path
from scipy.ndimage.filters import gaussian_filter1d


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
def get_number_of_comments_per_minute(chat_dataframe: pandas.DataFrame):
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

    # Append all the remaining items
    if count > 0:
        number_of_comments_per_minute['time_in_seconds'].append(current_time_in_seconds)
        number_of_comments_per_minute['number_of_comments'].append(count)

    return pd.DataFrame(number_of_comments_per_minute)


@time_it
def get_number_of_comments_per_unit_time_seconds(chat_dataframe: pandas.DataFrame, unit_time_seconds: int = 60):
    """Return a dataframe of number of comments per unit time in seconds

    Args:
        chat_dataframe: A panda dataframe that contains time_in_seconds and message
        unit_time_seconds:
            Duration in seconds used to count the number of comments.
            For example, unit_time_seconds = 30 will count the number of comments for every 30 seconds.
            Defaults to 60 seconds

    Returns:
        A dataframe of number of comments per unit time in seconds
    """
    number_of_comments_per_minute = {
        'time_in_seconds': [],
        'number_of_comments': [],
    }
    current_time_in_seconds = chat_dataframe['time_in_seconds'][0]
    count = 0

    for index in range(len(chat_dataframe)):
        if chat_dataframe['time_in_seconds'][index] > (current_time_in_seconds + unit_time_seconds):
            number_of_comments_per_minute['time_in_seconds'].append(current_time_in_seconds)
            number_of_comments_per_minute['number_of_comments'].append(count)
            current_time_in_seconds = chat_dataframe['time_in_seconds'][index]
            count = 0
        else:
            count += 1

    # Append all the remaining items
    if count > 0:
        number_of_comments_per_minute['time_in_seconds'].append(current_time_in_seconds)
        number_of_comments_per_minute['number_of_comments'].append(count)

    return pd.DataFrame(number_of_comments_per_minute)


def format_func(x, pos):
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)

    # return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


@time_it
def plot_bar_graph_of_number_of_comments_per_unit_time_in_seconds(
        number_of_comments_per_unit_time_seconds: pandas.DataFrame,
        unit_time_seconds: int):
    """Plot and save the bar graph of the number of comments against time

    Args:
        number_of_comments_per_unit_time_seconds: A pandas dataframe that consists of time_in_seconds and messages
        unit_time_seconds: Duration in seconds used to plot the number of comments.
            This should be the same as the unit_time_seconds used in the
            function [get_number_of_comments_per_unit_time_seconds]

    Returns:

    """
    output_dir = r'./plots'
    os.makedirs(output_dir, exist_ok=True)

    plot_title = f'Bar graph of number of comments per [{unit_time_seconds}s] for [{video_title}]'
    x_axis = list(number_of_comments_per_unit_time_seconds['time_in_seconds'])
    y_axis = list(number_of_comments_per_unit_time_seconds['number_of_comments'])
    plt.bar(x_axis, y_axis, width=unit_time_seconds)
    plt.title(plot_title, wrap=True)
    plt.xlabel('Time(s)')
    plt.ylabel('Number of comments')
    plot_filename = plot_title
    plot_filepath = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_filepath)
    plt.figure()


@time_it
def plot_line_graph_of_number_of_comments_per_unit_time_in_seconds(
        number_of_comments_per_unit_time_seconds: pandas.DataFrame,
        unit_time_seconds: int):
    """Plot and save the line graph of the number of comments against time

    Args:
        number_of_comments_per_unit_time_seconds: A pandas dataframe that consists of time_in_seconds and messages
        unit_time_seconds: Duration in seconds used to plot the number of comments.
            This should be the same as the unit_time_seconds used in the
            function [get_number_of_comments_per_unit_time_seconds]

    Returns:

    """
    output_dir = r'./plots'
    os.makedirs(output_dir, exist_ok=True)

    plot_title = f'Line graph (smoothened, sigma=2) of number of comments per [{unit_time_seconds}s] for [{video_title}]'

    x_axis = list(number_of_comments_per_unit_time_seconds['time_in_seconds'])
    x_axis_hhmmss = [(timedelta(seconds=second)) for second in x_axis]

    y_axis = list(number_of_comments_per_unit_time_seconds['number_of_comments'])
    y_smoothed = gaussian_filter1d(y_axis, sigma=2)

    fig, ax = plt.subplots(1)
    ax.plot(x_axis, y_smoothed)

    formatter = FuncFormatter(format_func)
    ax.xaxis.set_major_formatter(formatter)

    # plt.figure(figsize=(15,10))
    # plt.grid()
    # plt.plot(x_axis, y_smoothed)
    # plt.title(plot_title, wrap=True)
    # plt.locator_params(axis='x', nbins=10)
    # plt.xlabel('Time(s)')
    # plt.ylabel('Number of comments')
    # plot_filename = plot_title
    # plot_filepath = os.path.join(output_dir, plot_filename)
    # plt.savefig(plot_filepath)
    # plt.figure()


if __name__ == '__main__':

    all_chat_paths = glob.glob('./chats/*.csv')

    for chat_filepath in tqdm(all_chat_paths, total=len(all_chat_paths)):
        video_title = Path(chat_filepath).stem
        chat_dataframe = pd.read_csv(chat_filepath)
        unit_time_seconds_list = [60]

        for unit_time_seconds in unit_time_seconds_list:
            number_of_comments_per_unit_time_seconds = get_number_of_comments_per_unit_time_seconds(chat_dataframe,
                                                                                                    unit_time_seconds)
            plot_line_graph_of_number_of_comments_per_unit_time_in_seconds(number_of_comments_per_unit_time_seconds,
                                                                           unit_time_seconds)
