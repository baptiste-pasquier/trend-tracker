import json

import tweepy
from kafka import KafkaProducer

from m2ds_data_stream_project.ingest_tweets import TweetStream, reset_stream
from m2ds_data_stream_project.tools import load_config


def main():
    """
    Python Scripts to scrape raw twitter data and send it to a Kafka Producer
    """
    # Load config
    config = load_config("config.yml")
    secret_config = load_config("secret_config.yml")

    # Define Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=config["bootstrap_endpoint"],
        value_serializer=lambda m: json.dumps(m).encode("utf8"),
    )

    # Define Twitter stream client
    tweet_stream = TweetStream(
        bearer_token=secret_config["TWITTER"]["BEARER_TOKEN"],
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
    print(tweet_stream.get_rules())

    # Filtered stream
    tweet_stream.filter(
        expansions=["author_id", "geo.place_id"],
        tweet_fields=["created_at", "lang"],
        place_fields=["country", "name", "place_type"],
    )


if __name__ == "__main__":
    main()
