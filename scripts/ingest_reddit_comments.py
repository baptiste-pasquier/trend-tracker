import pandas as pd
import praw 
import time

from kafka import KafkaProducer

from m2ds_data_stream_project.tools import load_config

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
            "client_id":secret_config["REDDIT"]["CLIENT_ID"],
            "client_secret":secret_config["REDDIT"]["SECRET_TOKEN"], 
            "password":secret_config["REDDIT"]["REDDIT_PASSWORD"],
            "user_agent":secret_config["REDDIT"]["USER_AGENT"], 
            "username":secret_config["REDDIT"]["USERNAME"],
            "check_for_async":False
            }
    reddit = praw.Reddit(**args_reddit)

    subreddit = reddit.subreddit('news')

    for comment in subreddit.stream.comments():
        try:
            print(30*'_')
            print()
            parent_id = str(comment.parent())
            submission = reddit.comment(parent_id)
            reddit_data = {
                "id_comment": comment.id,
                "dt_created": comment.created_utc,
                "id_author": comment.author.id,
                "lang": "en", #99% is english text might need to investigate a bit more though | lib langid to test 
                "text": comment.body,
                "source":"reddit"
            }
            print(reddit_data)
            topic = config['raw_topic_reddit']
            producer.send(topic, tweet_data)
            log.info(f"Sending message to topic: {topic}\n{tweet_data}\n")
            time.sleep(config["time_sleep"])
        except praw.exceptions.PRAWException as e:
            pass
if __name__ == "__main__":
    main()