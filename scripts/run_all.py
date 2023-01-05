import logging.config
import threading

import cluster_data
import ingest_tweets
import tsf_data

if __name__ == "__main__":
    logging.config.fileConfig("logging_run_all.ini")
    threads = [
        threading.Thread(target=ingest_tweets.main),
        threading.Thread(target=tsf_data.main),
        threading.Thread(target=cluster_data.main),
    ]

    for thread in threads:
        thread.start()
