# wordle-github-contributions

Tweets your monthly GitHub Contributions as Wordle grid

![tweet](https://user-images.githubusercontent.com/25265451/153467247-3e996b0b-29bf-44db-8a6e-e8f26ad6959f.png)

### with tweepy support
```yml
name: Wordle GitHub Contributions

on:
  schedule:
    # at 08:00 on day-of-month 1
    - cron: "0 8 1 * *"

jobs:
  tweet-contribution-chart:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: vchrombie/wordle-github-contributions@master
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TWITTER_CONSUMER_KEY: ${{ secrets.TWITTER_CONSUMER_KEY }}
          TWITTER_CONSUMER_SECRET: ${{ secrets.TWITTER_CONSUMER_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
```
