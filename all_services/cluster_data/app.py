import json
import logging
import logging.config

from kafka import KafkaConsumer, KafkaProducer
from river import cluster, feature_extraction

from trend_tracker.utils import format_text_logging, load_config

log = logging.getLogger("cluster_data")


def main():
    """Streaming clustering of messages."""
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

    model = feature_extraction.BagOfWords(ngram_range=(1, 1))
    model |= cluster.TextClust(
        fading_factor=0.001,
        tgap=100,
        real_time_fading=False,
        num_macro=config["num_clusters"],
        auto_r=True,
    )

    for i, data in enumerate(consumer):
        if i % 10 == 0:
            log.info("_" * (3 + 100 + 4 + 7 + 4 + 7 + 3))
            log.info(
                f"""|| {"Text".center(100)} || Cluster || {"Source".center(7)} ||"""
            )
            log.info("-" * (3 + 100 + 4 + 7 + 4 + 7 + 3))
        data = data.value
        data["cluster"] = model.predict_one(data["text"], type="macro")
        try:
            model = model.learn_one(data["text"])
        except UnboundLocalError:
            pass
        log.info(
            f"""|| {format_text_logging(data["text"], 100, ljust=True)} || {str(data["cluster"]).center(7)} || {data["source"].center(7)} ||"""
        )
        producer.send(config["cluster_topic"], data)


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
