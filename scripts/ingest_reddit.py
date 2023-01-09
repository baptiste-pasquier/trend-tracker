import json
import logging
import logging.config
import time
from datetime import datetime

import praw
from kafka import KafkaProducer

from m2ds_data_stream_project.tools import load_config

log = logging.getLogger("ingest_reddit")


def main():
    # Load config
    secret_config = load_config("secret_config.yml")
    config = load_config("config.yml")

    # Define Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=config["bootstrap_endpoint"],
        value_serializer=lambda m: json.dumps(m).encode("utf8"),
    )

    args_reddit = {
        "client_id": secret_config["REDDIT"]["CLIENT_ID"],
        "client_secret": secret_config["REDDIT"]["CLIENT_SECRET"],
        "password": secret_config["REDDIT"]["PASSWORD"],
        "user_agent": secret_config["REDDIT"]["USER_AGENT"],
        "username": secret_config["REDDIT"]["USERNAME"],
        "check_for_async": False,
    }
    reddit = praw.Reddit(**args_reddit)

    log.info(f"Authenticated with username {reddit.user.me()}")

    subreddit = reddit.subreddit("news")

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
            log.info(f"Sending message to topic: {topic}\n{reddit_data}\n")
            time.sleep(config["time_sleep"])
        except praw.exceptions.PRAWException:
            pass


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
