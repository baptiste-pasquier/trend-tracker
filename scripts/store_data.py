import datetime
import json
import logging
import logging.config

import pymongo.errors
from dateutil import parser
from kafka import KafkaConsumer
from pymongo import MongoClient

from m2ds_data_stream_project.tools import format_text_logging, load_config

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
    try:
        client.admin.command("ping")
        log.info("Connected")
    except pymongo.errors.ConnectionFailure:
        log.error("Server not available")

    database = client["m2ds_data_stream"]
    collections = {"twitter": database["twitter"], "reddit": database["reddit"]}

    for i, message in enumerate(consumer):
        if i % 15 == 0:
            log.info("_" * (3 + 8 + 4 + 20 + 4 + 80 + 4 + 7 + 3))
            log.info(
                f"""|| Database || {"_id".center(20)} || {"Text".center(80)} || Cluster ||"""
            )
            log.info("-" * (3 + 8 + 4 + 20 + 4 + 80 + 4 + 7 + 3))

        data = message.value
        data["dt_created"] = parser.parse(data["dt_created"])
        data["dt_storage"] = datetime.datetime.utcnow()

        source = data["source"]
        try:
            log.info(
                f"""|| {source.center(8)} || {data.get("_id", "").center(20)} || {format_text_logging(data["text"], 80, ljust=True)} || {str(data["cluster"]).center(7)} ||"""
            )
            collections[source].insert_one(data)
        except pymongo.errors.DuplicateKeyError:
            log.warning("Trying to insert a duplicate key")


if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    main()
