import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from github import GitHubContributionsData

load_dotenv()

GH_USERNAME = os.getenv("INPUT_GH_USERNAME")
TITLE = os.getenv("INPUT_TITLE")
SHOW_MONTH = os.getenv("INPUT_SHOW_MONTH")
OUTPUT_FILE = os.getenv("INPUT_OUTPUT_FILE")
MARKER_START = os.getenv("INPUT_MARKER_START")
MARKER_END = os.getenv("INPUT_MARKER_END")
SVG_FILE = os.getenv("INPUT_SVG_FILE")

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


def generate_svg_grid(streak_matrix):
    """
    Create an SVG grid for the contribution streak.

    :param streak_matrix: matrix containing the values of the contribution streak
    :return: svg string
    """
    rows = len(streak_matrix)
    columns = len(streak_matrix[0]) if rows else 0
    cell = 12
    gap = 2
    width = columns * cell + max(columns - 1, 0) * gap
    height = rows * cell + max(rows - 1, 0) * gap

    contributed_color = "#2da44e"
    empty_color = "#d0d7de"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub contributions grid">'
    ]
    for row_index, row in enumerate(streak_matrix):
        for col_index, item in enumerate(row):
            if item == -1:
                continue
            x = col_index * (cell + gap)
            y = row_index * (cell + gap)
            color = contributed_color if item == 1 else empty_color
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" ry="2" fill="{color}"/>')
    parts.append("</svg>")
    return "".join(parts)


def build_markdown(title, month_label, svg_path, show_month):
    """
    Build markdown for the wordle grid

    :param title: heading text
    :param month_label: month and year label
    :param svg_path: path to the generated svg
    :param show_month: flag for rendering the month label
    :return: markdown string
    """
    parts = []
    if title:
        parts.append(f"### {title}")
    if show_month == 'True' and month_label:
        parts.append(f"#### {month_label}")
    parts.append(f'<img alt="GitHub contributions grid" src="{svg_path}" />')
    return "\n".join(parts)


def write_svg_file(svg_content, output_file, svg_file):
    """
    Write svg content to disk and return a relative path for README embedding.
    """
    if output_file:
        base_dir = os.path.dirname(output_file) or "."
    else:
        base_dir = "."

    svg_path = os.path.join(base_dir, svg_file)
    with open(svg_path, "w", encoding="utf-8") as handle:
        handle.write(svg_content)

    return svg_path


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
    svg = generate_svg_grid(streak_matrix)
    svg_path = write_svg_file(svg, OUTPUT_FILE, SVG_FILE)
    content = build_markdown(TITLE, month_label, svg_path, SHOW_MONTH)

    set_github_output("content", content)
    update_file_contents(OUTPUT_FILE, MARKER_START, MARKER_END, content)


if __name__ == '__main__':
    main()
