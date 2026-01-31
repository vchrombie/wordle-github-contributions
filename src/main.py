import os
from datetime import datetime, timedelta

from github import GitHubContributionsData

GREEN_SQUARE = '🟩'
BLACK_SQUARE = '⬛'
EMPTY_CHARS = '     '

GH_USERNAME = os.environ["INPUT_GH_USERNAME"]
TITLE = os.environ["INPUT_TITLE"]
SHOW_MONTH = os.environ["INPUT_SHOW_MONTH"]
OUTPUT_FILE = os.environ["INPUT_OUTPUT_FILE"]
MARKER_START = os.environ["INPUT_MARKER_START"]
MARKER_END = os.environ["INPUT_MARKER_END"]


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


def build_markdown(title, month_label, grid, show_month):
    """
    Build markdown for the wordle grid

    :param title: heading text
    :param month_label: month and year label
    :param grid: generated wordle grid
    :param show_month: flag for rendering the month label
    :return: markdown string
    """
    parts = []
    if title:
        parts.append(f"### {title}")
    if show_month == 'True' and month_label:
        parts.append(f"#### {month_label}")
    parts.append("<pre>")
    parts.append(grid.strip("\n"))
    parts.append("</pre>")
    return "\n".join(parts)


def set_github_output(name, value):
    """
    Write output to GitHub Actions output file when available
    """
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as handle:
            handle.write(f"{name}<<EOF\n{value}\nEOF\n")
    else:
        print(f"::set-output name={name}::{value}")


def update_file_contents(output_file, marker_start, marker_end, content):
    """
    Replace content between markers in the output file
    """
    if not output_file:
        return

    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Output file not found: {output_file}")

    with open(output_file, "r", encoding="utf-8") as handle:
        data = handle.read()

    start_index = data.find(marker_start)
    end_index = data.find(marker_end)

    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise ValueError("Markers not found or out of order in output file")

    start_index += len(marker_start)
    new_data = data[:start_index] + "\n" + content + "\n" + data[end_index:]

    with open(output_file, "w", encoding="utf-8") as handle:
        handle.write(new_data)


def main():
    """
    Generates your monthly GitHub Contributions as a Wordle grid
    """

    from_date, to_date = calculate_time_period()

    data = GitHubContributionsData().fetch_data(GH_USERNAME, from_date, to_date)
    months_data, weeks_data = data['months'], data['weeks']

    streak_matrix = generate_streak_matrix(weeks_data)

    month_label = '{} {}'.format(months_data[0]['name'], months_data[0]['year'])
    grid = generate_wordle_grid(streak_matrix)
    content = build_markdown(TITLE, month_label, grid, SHOW_MONTH)

    set_github_output("content", content)
    update_file_contents(OUTPUT_FILE, MARKER_START, MARKER_END, content)


if __name__ == '__main__':
    main()
