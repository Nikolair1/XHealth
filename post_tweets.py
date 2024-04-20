import tweepy
import os
from query_parser import parse_csv

# Environment vars
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")


# Authenticate with Twitter API and initialize the client
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)


def tweet():
    client.create_tweet(
        text="Hello Twitter world! This is my first tweet using .",
        user_auth=True,
    )
    print("success")


tweet()
