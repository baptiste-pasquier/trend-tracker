import json
import logging
import logging.config
import os
import time
from datetime import datetime

import praw
from dotenv import load_dotenv
from kafka import KafkaProducer

from trend_tracker.utils import format_text_logging, load_config

log = logging.getLogger("ingest_reddit")


def main():
    """Scrape raw Reddit data and send it to a Kafka Producer."""
    # Load config
    config = load_config("config.yml")
    load_dotenv()

    # Define Kafka producer
    time.sleep(config["time_wait_for_kafka"])
    producer = KafkaProducer(
        bootstrap_servers=config["bootstrap_endpoint"],
        value_serializer=lambda m: json.dumps(m).encode("utf8"),
    )

    args_reddit = {
        "client_id": os.environ["REDDIT_CLIENT_ID"],
        "client_secret": os.environ["REDDIT_CLIENT_SECRET"],
        "password": os.environ["REDDIT_PASSWORD"],
        "user_agent": os.environ["REDDIT_USER_AGENT"],
        "username": os.environ["REDDIT_USERNAME"],
        "check_for_async": False,
    }
    reddit = praw.Reddit(**args_reddit)

    log.info(f"Authenticated with username {reddit.user.me()}")

    subreddit = reddit.subreddit(config["subreddit"])

    for comment in subreddit.stream.comments():
        try:
            reddit_data = {
                "id_comment": comment.id,
                "dt_created": datetime.utcfromtimestamp(
                    comment.created_utc
                ).isoformat(),
                "id_author": comment.author.id,
                "lang": "en",  # 99% is english text might need to investigate a bit more though | lib langid to test
                "text": comment.body,
                "source": "reddit",
                "id_place": None,
                "place_country": None,
                "place_name": None,
                "place_type": None,
            }

            topic = config["raw_topic_reddit"]
            producer.send(topic, reddit_data)

            # Logging
            reddit_data["text"] = format_text_logging(reddit_data["text"], 100)
            log.info(f"Sending message to topic: {topic}\n{reddit_data}")

            time.sleep(config["time_sleep"])
        except praw.exceptions.PRAWException:
            pass


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
