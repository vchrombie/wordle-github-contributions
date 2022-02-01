# wordle-github-contributions
Tweets your monthly GitHub Contributions as Wordle boxes

### with tweepy support
```yml
name: Share your GitHub Contributions Chart as Wordle Grid on Twitter

on:
  schedule:
    # at 08:00 on day-of-month 1
    - cron: "0 8 1 * *"

jobs:
  contribution-chart:
    runs-on: ubuntu-latest
    steps:
      - name: Generate the contribution wordle chart
        uses: vchrombie/wordle-github-contributions@master
        with:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TWITTER_CONSUMER_KEY: ${{ secrets.TWITTER_CONSUMER_KEY }}
          TWITTER_CONSUMER_SECRET: ${{ secrets.TWITTER_CONSUMER_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
```
