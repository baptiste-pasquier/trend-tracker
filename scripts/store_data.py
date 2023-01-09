import datetime
import json
import logging
import logging.config

from dateutil import parser
from kafka import KafkaConsumer
from pymongo import MongoClient

from m2ds_data_stream_project.tools import load_config

log = logging.getLogger("store_data")


def main():
    # Load config
    secret_config = load_config("secret_config.yml")
    config = load_config("config.yml")

    consumer = KafkaConsumer(
        config["cluster_topic"],
        bootstrap_servers=config["bootstrap_endpoint"],
        group_id=config["group_id"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    client = MongoClient(secret_config["MONGODB"]["CONNECTION_STRING"])
    database = client["m2ds_data_stream"]
    collection_twitter = database["twitter"]
    collection_reddit = database["reddit"]

    for message in consumer:
        data = message.value

        data["dt_created"] = parser.parse(data["dt_created"])
        data["dt_storage"] = datetime.datetime.utcnow()

        if data["source"] == "twitter":
            collection_twitter.insert_one(data)
            log.info("Inserting one Twitter data")
        elif data["source"] == "reddit":
            collection_reddit.insert_one(data)
            log.info("Inserting one Reddit data")


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
