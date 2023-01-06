import json
import logging
import logging.config

import nltk
from kafka import KafkaConsumer, KafkaProducer

from m2ds_data_stream_project.tools import load_config, log_text
from m2ds_data_stream_project.tsf_data import text_cleaning

log = logging.getLogger("tsf_data")


def main():
    # Load config
    config = load_config("config.yml")

    #Load all the data sources
    topics = (config["raw_topic"],config["raw_topic_reddit"])

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
    i = 0
    for data in consumer:
        if i % 15 == 0:
            log.info("_" * (4 + 80 + 6 + 40 + 6 + 40 + 4))
            log.info(
                f"""||  {"Text".center(80)}  ||  {"Mentions".center(40)}  ||  {"Hashtags".center(40)}  ||"""
            )
            log.info("-" * (4 + 80 + 6 + 40 + 6 + 40 + 4))
        data = data.value
        log.info(f"""||  {log_text(data["text"], 80)}  ||{" "*44}||{" "*44}||""")
        data["text"], data["mentions"], data["hashtags"] = text_cleaning(
            data["text"],
            negation_set=set(config["negation_words"]),
            fg_stop_words=config["fg_stop_words"],
            fg_lemmatization=config["fg_lemmatization"],
        )
        log.info(
            f"""||  {log_text(data["text"], 80)}  ||  {log_text(str(data["mentions"]), 40)}  ||  {log_text(str(data["hashtags"]), 40)}  ||"""
        )
        i += 1

        # Send the preprocessed data
        producer.send(config["clean_topic"], data)


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
