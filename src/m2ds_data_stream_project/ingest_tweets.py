import json
import time

import tweepy


class TweetStream(tweepy.StreamingClient):
    """
    Customised Streaming Class
    """

    def __init__(self, producer, raw_topic, time_sleep, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = producer
        self.raw_topic = raw_topic
        self.time_sleep = time_sleep

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

        topic = self.raw_topic
        self.producer.send(topic, tweet_data)
        print(f"Sending message to topic: {topic}\n{tweet_data}\n")
        time.sleep(self.time_sleep)


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
