import os
import tweepy


class TweetContent:
    """
    Class to authenticate using the keys & secret tokens and
    sends tweet using the tweepy library.
    """

    def __init__(self):
        # twitter keys
        self.consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
        self.consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
        self.access_token = os.environ["TWITTER_ACCESS_TOKEN"]
        self.access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    def send_tweet(self, content):
        """
        Send the tweet of the Wordle grid

        :param content: content of the tweet
        """
        # authentication
        auth = tweepy.OAuth1UserHandler(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
        api = tweepy.API(auth)

        # send tweet
        api.update_status(status=content)

        print("tweeted!")
