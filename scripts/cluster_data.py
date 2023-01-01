import json

from kafka import KafkaConsumer, KafkaProducer
from river import cluster, feature_extraction, metrics

from m2ds_data_stream_project.tools import load_config


def main():
    # Load config
    config = load_config("config.yml")

    producer = KafkaProducer(
        bootstrap_servers=config["bootstrap_endpoint"],
        value_serializer=lambda m: json.dumps(m).encode("utf8"),
    )
    # Call a Consumer to retrieve the raw tweets

    consumer = KafkaConsumer(
        config["clean_topic"],
        bootstrap_servers=config["bootstrap_endpoint"],
        group_id=config["group_id"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    # tfidf = feature_extraction.TFIDF()
    # adj_rand_score = metrics.AdjusterRand()
    # silhouette_score = metrics.Silhouette()

    model = feature_extraction.BagOfWords(ngram_range=(1, 2))
    model |= cluster.TextClust(
        real_time_fading=False, fading_factor=0.001, tgap=100, auto_r=True
    )

    for data in consumer:
        data = data.value
        print(data["text"], "\n")
        data["cluster"] = model.predict_one(data["text"])
        model = model.learn_one(data["text"])
        print(data["cluster"])
        producer.send(config["cluster_topic"], data)


if __name__ == "__main__":
    main()
