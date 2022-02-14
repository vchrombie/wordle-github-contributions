import os
from datetime import datetime, timedelta

from github import GitHubContributionsData
from twitter import TweetContent

GREEN_SQUARE = '🟩'
BLACK_SQUARE = '⬛'
EMPTY_CHARS = '     '

GH_USERNAME = os.environ["INPUT_GH_USERNAME"]
TWEET_FLAG = os.environ["INPUT_TWEET_FLAG"]


def calculate_time_period():
    """
    Calculates the starting and ending time period of the previous month

    :return: from and to dates
    """
    to_date = datetime.now().replace(day=1).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
        microseconds=1)
    from_date = (to_date - timedelta(days=1)).replace(day=1).replace(hour=0, minute=0, second=0, microsecond=0)

    return from_date, to_date


def generate_streak_matrix(weeks_data):
    """
    Create the streak matrix
        1 if the user committed
        0 if the user hasn't committed
        -1 to store null values

    :param weeks_data: week-wise contribution data of the user
    :return: matrix containing the values of the contribution streak
    """
    rows, columns = 7, len(weeks_data)
    streak_matrix = [[-1 for i in range(columns)] for y in range(rows)]

    i = 0
    for week in weeks_data:
        days = week['contributionDays']
        for day in days:
            if day['contributionCount'] > 0:
                streak_matrix[day['weekday']][i] = 1
            elif day['contributionCount'] == 0:
                streak_matrix[day['weekday']][i] = 0
        i += 1

    return streak_matrix


def generate_wordle_grid(streak_matrix):
    """
    Create the Wordle grid

    :param streak_matrix: matrix containing the values of the contribution streak
    :return: wordle grid
    """
    grid = ''
    for row in streak_matrix:
        grid += '\n'
        for item in row:
            if item == 1:
                grid += GREEN_SQUARE
            elif item == 0:
                grid += BLACK_SQUARE
            else:
                grid += EMPTY_CHARS

    return grid


def main():
    """
    Tweets your monthly GitHub Contributions as Wordle grid
    """

    from_date, to_date = calculate_time_period()

    data = GitHubContributionsData().fetch_data(GH_USERNAME, from_date, to_date)
    months_data, weeks_data = data['months'], data['weeks']

    streak_matrix = generate_streak_matrix(weeks_data)

    tweet = '\n{} {}\n'.format(months_data[0]['name'], months_data[0]['year'])
    tweet += generate_wordle_grid(streak_matrix)
    tweet += '\n\n#wordle #github'

    print(f"::set-output name=tweet::{tweet}")

    if TWEET_FLAG == 'True':
        TweetContent().send_tweet(content=tweet)


if __name__ == '__main__':
    main()
