import json
import time

import nltk
from ingest_tweets import BOOTSTRAP_ENDPOINT, RAW_TOPIC, TIME_SLEEP
from kafka import KafkaConsumer, KafkaProducer

from m2ds_data_stream_project.tsf_data import text_cleaning

GROUP_ID = "main_group"
NEGATION_SET = {"no", "not"}
FG_STOP_WORDS = False
FG_LEMMATIZATION = False
CLEAN_TOPIC = "clean_tweets"


def main():
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("wordnet")

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_ENDPOINT,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )
    # Call a Consumer to retrieve the raw tweets
    consumer = KafkaConsumer(
        RAW_TOPIC,
        bootstrap_servers=BOOTSTRAP_ENDPOINT,
        group_id=GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    # Preprocess the tweets
    for data in consumer:
        data = data.value
        print(data["text"])
        print("tsf")
        data["text"], data["mentions"], data["hashtags"] = text_cleaning(
            data["text"],
            negation_set=NEGATION_SET,
            fg_stop_words=FG_STOP_WORDS,
            fg_lemmatization=FG_LEMMATIZATION,
        )
        print(data["text"], data["mentions"], data["hashtags"])

        # Send the preprocessed data
        producer.send(CLEAN_TOPIC, data)

        time.sleep(TIME_SLEEP)


if __name__ == "__main__":
    main()
