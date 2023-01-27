import json
import logging
import logging.config

import nltk
from kafka import KafkaConsumer, KafkaProducer
from utils import text_cleaning

from trend_tracker.utils import format_text_logging, load_config

log = logging.getLogger("tsf_data")


def main():
    """Preprocess tweets and Reddit messages."""
    # Load config
    config = load_config("config.yml")

    # Load all the data sources
    topics = (config["raw_topic"], config["raw_topic_reddit"])

    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("wordnet")

    producer = KafkaProducer(
        bootstrap_servers=config["bootstrap_endpoint"],
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    # Call a Consumer to retrieve the raw tweets
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=config["bootstrap_endpoint"],
        group_id=config["group_id"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    # Preprocess the tweets
    for i, data in enumerate(consumer):
        if i % 15 == 0:
            log.info("_" * (3 + 80 + 4 + 35 + 4 + 35 + 4 + 7 + 3))
            log.info(
                f"""|| {"Text".center(80)} || {"Mentions".center(35)} || {"Hashtags".center(35)} || {"Source".center(7)} ||"""
            )
            log.info("-" * (3 + 80 + 4 + 35 + 4 + 35 + 4 + 7 + 3))
        data = data.value
        log.info(
            f"""|| {format_text_logging(data["text"], 80, ljust=True)} || {" "*35} || {" "*35} || {" "*7} ||"""
        )
        data["text"], data["mentions"], data["hashtags"] = text_cleaning(
            data["text"],
            negation_set=set(config["negation_words"]),
            fg_stop_words=config["fg_stop_words"],
            fg_lemmatization=config["fg_lemmatization"],
        )
        log.info(
            f"""|| {format_text_logging(data["text"], 80, ljust=True)} || {format_text_logging(str(data["mentions"]), 35, ljust=True)} || {format_text_logging(str(data["hashtags"]), 35, ljust=True)} || {data["source"].center(7)} ||"""
        )

        # Send the preprocessed data
        producer.send(config["clean_topic"], data)


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
