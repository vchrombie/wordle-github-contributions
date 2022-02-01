import os
import requests
import tweepy

from datetime import datetime, timedelta
from requests_oauthlib import OAuth1Session


GREEN_SQUARE = '🟩'
BLACK_SQUARE = '⬛'
EMPTY_CHARS = '     '

GH_TOKEN = os.environ["GH_TOKEN"]
HEADERS = {'Authorization': 'Bearer {}'.format(GH_TOKEN)}

QUERY = """
query($username:String!, $from_date:DateTime!, $to_date:DateTime) {
  user(login: $username) {
    contributionsCollection(
      from: $from_date, 
      to: $to_date
    ) {
      contributionCalendar {
        months {
          name
          year
          totalWeeks
        }
        weeks {
          contributionDays {
            contributionCount
            weekday
          }
        }
      }
    }
  }
}
"""

to_date = datetime.now().replace(day=1).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)
from_date = (to_date - timedelta(days=1)).replace(day=1).replace(hour=0, minute=0, second=0, microsecond=0)

VARIABLES = {
    "username": os.environ["GH_USERNAME"],
    "from_date": from_date.isoformat(),
    "to_date": to_date.isoformat(),
}

body = {
    "query": QUERY,
    "variables": VARIABLES
}

response = requests.post(
    'https://api.github.com/graphql',
    json=body,
    headers=HEADERS,
)

data = response.json()
data = data['data']['user']['contributionsCollection']['contributionCalendar']
months_data, weeks_data = data['months'], data['weeks']

total_weeks = months_data[0]['totalWeeks']

rows, columns = 7, total_weeks
month_table = [[-1 for i in range(columns)] for y in range(rows)]


i = 0
for week in weeks_data:
    days = week['contributionDays']
    for day in days:
        if day['contributionCount'] > 0:
            month_table[day['weekday']][i] = 1
        elif day['contributionCount'] == 0:
            month_table[day['weekday']][i] = 0
    i += 1

tweet = '\n{} {}\n'.format(months_data[0]['name'], months_data[0]['year'])
for row in month_table:
    tweet += '\n'
    for item in row:
        if item == 1:
            tweet += GREEN_SQUARE
        elif item == 0:
            tweet += BLACK_SQUARE
        else:
            tweet += EMPTY_CHARS
tweet += '\n\n#wordle #github'

print(f"::set-output name=tweet::{tweet}")


if os.environ["TWEET_FLAG"] == 'True':
    # twitter keys
    consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    # authentication
    auth = tweepy.OAuth1UserHandler(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    api = tweepy.API(auth)

    # send tweet
    result = api.update_status(status=tweet)

    print("tweeted!")


# if __name__ == '__main__':
#     main()
