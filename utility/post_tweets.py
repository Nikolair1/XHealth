import tweepy
import os
import requests


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


topics = [
    "Daily Health Advice 🍏",
    "Disease Outbreaks and Public Health Emergencies 🚨",
    "Health Disparities and Equity 🤲",
    "Medical Research and Innovations 🧬",
]


# topics is a dicitonary from topic -> topic summary
def tweet(summary, topic_summaries, date):
    # print("ARGS ARE ", summary)
    print(len(summary))

    text = "Weekly Summary " + date + " 📋 \n"
    for topic, emoji in zip(summary, topics):
        text += emoji[-1] + " " + topic + "\n"

    summary_later = text
    response = client.create_tweet(
        text=text,
        user_auth=True,
    )

    print(response)

    counter = 0
    while counter < 4:
        print("Length of topic is ", len(topic_summaries[counter]))
        client.create_tweet(
            text=topics[counter][-1] + " " + topic_summaries[counter],
            user_auth=True,
            in_reply_to_tweet_id=response.data["id"],
        )
        counter += 1

    # SAVE tweet data and link in flask DB
    flask_endpoint = "http://127.0.0.1:5000/add_tweet"
    # Construct the data dictionary
    data = {
        "summary": summary_later,
        "topic1": topic_summaries[0],  # Assign the first topic summary to topic1
        "topic2": topic_summaries[1],  # Assign the second topic summary to topic2
        "topic3": topic_summaries[2],  # Assign the third topic summary to topic3
        "topic4": topic_summaries[3],  # Assign the fourth topic summary to topic4
        "link": "https://twitter.com/_nicky_2/status/" + response.data["id"],
        "date": "2024-04-21",
    }
    response = requests.post(flask_endpoint, json=data)
    if response.status_code == 200:
        print("Tweet saved successfully")
    else:
        print("Failed to save tweet")


# testing
# summary = (
#     "Our first summary focuses on Bird Flu and good advice from reputable doctors."
# )
# topic_summaries = [
#     "1Eat an apple a day!",
#     "1Measles is at an all time low!",
#     "1Bird flu affects different social classes differently.",
#     "1Researchers found huge potential of weight-loss drugs like Ozempic and Wegovy, and their implications for public health and medical research.",
# ]
# tweet(summary, topic_summaries)
