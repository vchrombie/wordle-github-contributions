import os
import requests


class GitHubContributionsData:
    """
    This class fetches the monthly contributions data using the
    GitHub GraphQL API.
    """

    def __init__(self):
        self.headers = {'Authorization': 'Bearer {}'.format(os.environ["GH_TOKEN"])}
        self.query = """        
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

    def fetch_data(self, username, from_date, to_date):
        """
        Fetches the contributions data of the `username` during the previous month

        :param username: github username
        :param from_date: date from which the contributions data is to be fetched
        :param to_date: date till which the contributions data is to be fetched
        :return: contributions JSON data
        """
        variables = {
            "username": username,
            "from_date": from_date.isoformat(),
            "to_date": to_date.isoformat(),
        }

        body = {
            "query": self.query,
            "variables": variables
        }

        response = requests.post(
            'https://api.github.com/graphql',
            json=body,
            headers=self.headers,
        )

        data = response.json()
        data = data['data']['user']['contributionsCollection']['contributionCalendar']

        return data
