# wordle-github-contributions

Tweets your monthly GitHub Contributions as Wordle grid

![tweet](https://user-images.githubusercontent.com/25265451/153467247-3e996b0b-29bf-44db-8a6e-e8f26ad6959f.png)

---

## Instructions

Create a workflow file in any of your repository ([example](https://github.com/vchrombie/vchrombie/blob/master/.github/workflows/wordle-github.yml))

`.github/workflows/tweet-wordle-github.yml`
```yml
name: Wordle GitHub Contributions

on:
  schedule:
    # at 08:00 on the 1st of every month
    - cron: "0 8 1 * *"

jobs:
  tweet-contribution-grid:
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

The above job runs at 0800 UTC, on the 1st of every month. You can change it as you wish based on the [cron syntax](https://jasonet.co/posts/scheduled-actions/#the-cron-syntax). 

It fetches your contribution data of the last month, generates the wordle grid and tweets it.

### Override defaults

| Input Param | Default Value | Description |
|--------|--------|--------|
| `TWEET_FLAG` | True | Flag variable to use the in-built tweepy library to tweet the wordle grid |

If you decide not to tweet it, you can set the `TWEET_FLAG` variable to `False`. You need not provide the Twitter API keys, tokens in that case.

```yml
jobs:
  contribution-grid:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: vchrombie/wordle-github-contributions@master
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          TWEET_FLAG: False
```

### Use other actions for sending the tweet

The tweet content is stored in the workflow output variable `tweet`. You can combine this worflow to send a tweet using different github actions like [ethomson/send-tweet-action](https://github.com/ethomson/send-tweet-action).

```yml
jobs:
  contribution-grid:
    runs-on: ubuntu-latest
    outputs:
      tweet: ${{ steps.generate_tweet.outputs.tweet }}
    steps:
      - uses: actions/checkout@v2
      - uses: vchrombie/wordle-github-contributions@master
        id: generate_tweet
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          TWEET_FLAG: False
  tweet:
    runs-on: ubuntu-latest
    needs: contribution-grid
    steps:
      - uses: ethomson/send-tweet-action@v1
        with:
          status: ${{ needs.contribution-grid.outputs.tweet }}
          consumer-key: ${{ secrets.TWITTER_CONSUMER_API_KEY }}
          consumer-secret: ${{ secrets.TWITTER_CONSUMER_API_SECRET }}
          access-token: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          access-token-secret: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
```
