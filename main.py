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


# Saves all tweets to output file, run carefully
def search_all_and_save(output_file, data_filename):
    account_names = parse_csv(data_filename)
    with open(output_file, "w") as f:
        for name in account_names:
            query = "from:" + name + " -is:retweet"
            results = search_one(query)
            f.write("Account Name: " + name + "-------------------" + "\n")
            for result in results:
                f.write(result + "\n")


def search_one(query):
    search_results = client.search_recent_tweets(query=query)
    res = []
    for tweet in search_results.data:
        res.append(tweet.text)
    return res


"""
query = "from:_nicky_2 -is:retweet"
res = search_one(query)
print(res)

Outputs: [<Tweet id=1780002836904059043 text='Hello World!'>, <Tweet id=1780000896002531621 text='Hello world again!'>]
"""

# search_all_and_save("debug_results.txt", "debug.csv")