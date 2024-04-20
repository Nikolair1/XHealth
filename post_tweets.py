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


# topics is a dicitonary from topic -> topic summary
def tweet(summary, topics):
    text = "Weekly Summary 💊🏥🩺📋 \n" + summary + "\n\nTopics:\n"
    for i, topic in enumerate(topics):
        text += topic + "\n"

    response = client.create_tweet(
        text=text,
        user_auth=True,
    )
    counter = 1
    for topic in topics:
        client.create_tweet(
            text=topic[-1] + " " + topics[topic],
            user_auth=True,
            in_reply_to_tweet_id=response.data["id"],
        )
        counter += 1


# testing
summary = (
    "Our first summary focuses on Bird Flu and good advice from reputable doctors."
)
topics = {
    "Daily Health Advice 🍏": "Eat an apple a day!",
    "Disease Outbreaks and Public Health Emergencies 🚨": "Measles is at an all time low!",
    "Health Disparities and Equity 🤲": "Bird flu affects different social classes differently.",
    "Medical Research and Innovations 🧬": "Researchers found huge potential of weight-loss drugs like Ozempic and Wegovy, and their implications for public health and medical research.",
}
tweet(summary, topics)
