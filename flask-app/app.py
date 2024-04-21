from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from datetime import datetime, date
from flask import jsonify, request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(
        db.String(280), nullable=False
    )  # Assuming a max of 280 characters for tweet summary
    topic1 = db.Column(db.String(280))
    topic2 = db.Column(db.String(280))
    topic3 = db.Column(db.String(280))
    topic4 = db.Column(db.String(280))
    date = db.Column(db.Date, default=date.today)
    link = db.Column(db.String(200))  # Adjust the max length as needed for your URLs

    def __repr__(self):
        return f"<Tweet {self.id}>"


# Create the database tables
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

# Sample data for past weeks
past_weeks_data = {
    "Week 1": "Text for Week 1",
    "Week 2": "Text for Week 2",
}


@app.route("/tweets", methods=["GET"])
def get_tweets():
    # Query all tweets from the database
    tweets = Tweet.query.all()

    # Serialize the tweets to JSON format
    serialized_tweets = []
    for tweet in tweets:
        serialized_tweet = {
            "id": tweet.id,
            "summary": tweet.summary,
            "topic1": tweet.topic1,
            "topic2": tweet.topic2,
            "topic3": tweet.topic3,
            "topic4": tweet.topic4,
            "date": tweet.date.strftime("%Y-%m-%d"),
            "link": tweet.link,
        }
        serialized_tweets.append(serialized_tweet)

    # Return the serialized tweets as JSON
    return jsonify(serialized_tweets)


@app.route("/add_tweet", methods=["POST"])
def add_tweet():
    # Get data from the request body as JSON
    data = request.json

    # Extract data from JSON
    summary = data.get("summary")
    topic1 = data.get("topic1")
    topic2 = data.get("topic2")
    topic3 = data.get("topic3")
    topic4 = data.get("topic4")
    link = data.get("link")
    tweet_date_str = data.get("date")

    # Convert date string to datetime object
    if tweet_date_str:
        try:
            tweet_date = datetime.strptime(tweet_date_str, "%Y-%m-%d")
        except ValueError:
            return (
                jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD"}),
                400,
            )
    else:
        # If no date provided, use current date
        tweet_date = datetime.now()

    # Check if required fields are present
    if summary is None:
        return jsonify({"error": "Summary is required"}), 400

    # Create a new tweet object with the provided data and date
    new_tweet = Tweet(
        summary=summary,
        topic1=topic1,
        topic2=topic2,
        topic3=topic3,
        topic4=topic4,
        date=tweet_date,
        link=link,
    )

    # Add the tweet to the database session and commit changes
    db.session.add(new_tweet)
    db.session.commit()

    return jsonify({"message": "Tweet added successfully"})


@app.route("/")
def index():
    # Retrieve the most recent tweet
    most_recent_tweet = Tweet.query.order_by(Tweet.date.desc()).first()
    print(most_recent_tweet)
    # Render the template with the most recent tweet and past weeks data
    return render_template(
        "./index.html", most_recent_tweet=most_recent_tweet, weeks=past_weeks_data
    )


@app.route("/past_tweets")
def past_tweets():
    # Retrieve all past tweets
    past_tweets = Tweet.query.all()
    return render_template("past_weeks.html", past_tweets=past_tweets)


if __name__ == "__main__":
    app.run(debug=True)
