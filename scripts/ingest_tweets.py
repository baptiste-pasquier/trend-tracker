import json
import os
import time

import tweepy

from kafka import KafkaProducer

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
RAW_TOPIC = "raw_tweets"
BOOTSTRAP_ENDPOINT = "localhost:9092"
STREAM_RULE = "news lang:en has:geo -is:retweet"
TIME_SLEEP = 0.5


class TweetStream(tweepy.StreamingClient):
    """
    Customised Streaming Class
    """

    def __init__(self, producer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = producer

    def on_connect(self):
        print("connected")

    def on_data(self, tweet):
        """
        Function called when a new tweet is detected. The data is selected and send to a Producer

        Arguments
        -------------------------
                tweet(<bytes>): Data regarding the tweet
                producer(<KafkaProducer>): Producer to retrieve raw data
        """
        tweet = json.loads(tweet)
        tweet_data = {
            "id": tweet["data"]["id"],
            "created_at": tweet["data"]["created_at"],
            "author_id": tweet["data"]["author_id"],
            "lang": tweet["data"]["lang"],
            "place_id": tweet["data"]["geo"]["place_id"],
            "place_country": tweet["includes"]["places"][0]["country"],
            "place_name": tweet["includes"]["places"][0]["name"],
            "place_type": tweet["includes"]["places"][0]["place_type"],
            "text": tweet["data"]["text"],
        }

        topic = RAW_TOPIC
        self.producer.send(topic, tweet_data)
        print(f"Sending message to topic: {topic}\n{tweet_data}\n")
        time.sleep(TIME_SLEEP)


def reset_stream(tweet_stream):
    """
    Reset all the rules regarding a Streaming Client (not automatic after stopping execution)

    Arguments
    -----------------------
            tweet_stream(<TweetStream>): Object to reset the rules on

    """
    rules = tweet_stream.get_rules()
    ids = [r.id for r in rules.data]
    tweet_stream.delete_rules(ids)


def main():
    """
    Python Scripts to scrape raw twitter data and send it to a Kafka Producer
    """

    # Define Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_ENDPOINT,
        value_serializer=lambda m: json.dumps(m).encode("utf8"),
    )

    # Define Twitter stream client
    tweet_stream = TweetStream(bearer_token=BEARER_TOKEN, producer=producer)
    previous_rules = tweet_stream.get_rules().data

    # Delete previous rules
    if previous_rules:
        reset_stream(tweet_stream)

        # Add new rules
    rule = tweepy.StreamRule(STREAM_RULE)
    tweet_stream.add_rules(rule)
    print(tweet_stream.get_rules())

    # Filtered stream
    tweet_stream.filter(
        expansions=["author_id", "geo.place_id"],
        tweet_fields=["created_at", "lang"],
        place_fields=["country", "name", "place_type"],
    )


if __name__ == "__main__":
    main()
