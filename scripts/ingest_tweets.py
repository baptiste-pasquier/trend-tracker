import json
import os

import tweepy
from kafka import KafkaProducer

from m2ds_data_stream_project.ingest_tweets import TweetStream, reset_stream

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
RAW_TOPIC = "raw_tweets"
BOOTSTRAP_ENDPOINT = "localhost:9092"
STREAM_RULE = "news lang:en has:geo -is:retweet"
TIME_SLEEP = 0.2


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
    tweet_stream = TweetStream(
        bearer_token=BEARER_TOKEN,
        producer=producer,
        raw_topic=RAW_TOPIC,
        time_sleep=TIME_SLEEP,
    )
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
