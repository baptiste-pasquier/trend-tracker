import json
import time

import tweepy
from kafka import KafkaProducer


class TweetStream(tweepy.StreamingClient):
    """
    Customised Streaming Class
    """

    def __init__(
        self,
        producer: KafkaProducer,
        raw_topic: str,
        time_sleep: float,
        *args,
        **kwargs,
    ):
        """
        Parameters
        ----------
        producer : KafkaProducer
            Producer to retrieve raw data
        raw_topic : str
            Topic kafka where to send tweets
        time_sleep : float
            Sleep time between each tweet
        """
        super().__init__(*args, **kwargs)
        self.producer = producer
        self.raw_topic = raw_topic
        self.time_sleep = time_sleep

    def on_connect(self):
        print("connected")

    def on_data(self, raw_data: bytes):
        """Function called when a new tweet is detected. The data is selected and send to a Producer

        Parameters
        ----------
        raw_data : bytes
            Data regarding the tweet
        """
        tweet = json.loads(raw_data)
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

        topic = self.raw_topic
        self.producer.send(topic, tweet_data)
        print(f"Sending message to topic: {topic}\n{tweet_data}\n")
        time.sleep(self.time_sleep)


def reset_stream(tweet_stream: TweetStream) -> None:
    """Reset all the rules regarding a Streaming Client (not automatic after stopping execution)

    Parameters
    ----------
    tweet_stream : TweetStream
        Object to reset the rules on
    """
    rules = tweet_stream.get_rules()
    ids = [r.id for r in rules.data]
    tweet_stream.delete_rules(ids)
