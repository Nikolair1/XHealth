import tweepy
import os
from query_parser import parse_csv
from datetime import datetime
import time


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


# Saves all tweets to output file, run carefully
def search_all_and_save(output_file, data_filename, search_f):
    account_names = parse_csv(data_filename)
    with open(output_file, "w") as f:
        for name in account_names:
            query = "from:" + name + " -is:retweet"
            results = search_f(query)
            # f.write("Account Name: " + name + "-------------------" + "\n")
            for result in results:
                cleaned_result = result.replace("\n", "")
                f.write(cleaned_result + "\n")


def search_one(query):
    search_results = client.search_recent_tweets(query=query)
    res = []
    if search_results.data is not None:
        for tweet in search_results.data:
            if tweet:
                res.append(tweet.text)
    return res


def search_one_historic(query):
    # Introduce a delay of 0.5 seconds before making the next request
    time.sleep(5)
    start_time = datetime(2024, 3, 31).isoformat() + "Z"
    end_time = datetime(2024, 4, 7).isoformat() + "Z"
    search_results = client.search_all_tweets(
        query=query, start_time=start_time, end_time=end_time
    )
    res = []
    if search_results.data is not None:
        for tweet in search_results.data:
            if tweet:
                res.append(tweet.text)
    return res


search_all_and_save("april_7_tweets.txt", "../data/accounts.csv", search_one_historic)
