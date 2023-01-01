import json

import nltk
from kafka import KafkaConsumer, KafkaProducer

from m2ds_data_stream_project.tools import load_config
from m2ds_data_stream_project.tsf_data import text_cleaning


def main():
    # Load config
    config = load_config("config.yml")

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
        config["raw_topic"],
        bootstrap_servers=config["bootstrap_endpoint"],
        group_id=config["group_id"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    # Preprocess the tweets
    for data in consumer:
        data = data.value
        print(data["text"])
        print("tsf")
        data["text"], data["mentions"], data["hashtags"] = text_cleaning(
            data["text"],
            negation_set=set(config["negation_words"]),
            fg_stop_words=config["fg_stop_words"],
            fg_lemmatization=config["fg_lemmatization"],
        )
        print(data["text"], data["mentions"], data["hashtags"])

        # Send the preprocessed data
        producer.send(config["clean_topic"], data)


if __name__ == "__main__":
    main()
