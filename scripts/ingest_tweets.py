import json
import logging
import logging.config
import os

import tweepy
from kafka import KafkaProducer

from trend_tracker.ingest_tweets import TweetStream, reset_stream
from trend_tracker.tools import load_config, load_config_in_environment

log = logging.getLogger("ingest_tweets")


def main():
    """Scrape raw Twitter data and send it to a Kafka Producer."""
    # Load config
    config = load_config("config.yml")
    load_config_in_environment("secret_config.yml", log)

    # Define Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=config["bootstrap_endpoint"],
        value_serializer=lambda m: json.dumps(m).encode("utf8"),
    )

    # Define Twitter stream client
    tweet_stream = TweetStream(
        bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
        producer=producer,
        raw_topic=config["raw_topic"],
        time_sleep=config["time_sleep"],
    )
    previous_rules = tweet_stream.get_rules().data

    # Delete previous rules
    if previous_rules:
        reset_stream(tweet_stream)

    # Add new rules
    rule = tweepy.StreamRule(config["stream_rule"])
    tweet_stream.add_rules(rule)
    log.info(tweet_stream.get_rules())

    # Filtered stream
    tweet_stream.filter(
        expansions=["author_id", "geo.place_id"],
        tweet_fields=["created_at", "lang"],
        place_fields=["country", "name", "place_type"],
    )


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
