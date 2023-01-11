import datetime

import matplotlib.pyplot as plt
import pandas as pd
import pymongo.errors
import streamlit as st
from pymongo import MongoClient
from pymongo_schema.extract import extract_pymongo_client_schema
from wordcloud import WordCloud


def make_wordCloud(words, id_cluster):
    """Plot a Wordcloud graph

    Parameters
    ----------
        words: str
            corpus to plot
        nb_cluster: int
            unique idenitifier of the cluster
    """
    wordcloud = WordCloud().generate(words)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.set_axis_off()
    st.markdown(f"Most popular hashtags of the cluster {id_cluster}")
    st.pyplot(fig)
    plt.close()


class DataVizMongoDB:
    def __init__(
        self,
        connection_string,
        logger,
    ):
        self.client = MongoClient(connection_string)
        try:
            self.client.admin.command("ping")
            logger.info("Connected")
        except pymongo.errors.ConnectionFailure:
            logger.error("Server not available")

        database = self.client["m2ds_data_stream"]

        self.collection_twitter = database["twitter"]
        self.collection_reddit = database["reddit"]

        self.last_query_time = datetime.datetime(1970, 1, 1)
        self.datetime_now = datetime.datetime.utcnow()

        self.data_memory_twitter = []
        self.data_memory_reddit = []
        self.count_memory = []

        self.df_data = pd.DataFrame([])
        self.df_count = pd.DataFrame([])

        self.logger = logger

        self.get_cluster_keys()

    def is_memory_empty(self):
        return len(self.data_memory_twitter) + len(self.data_memory_reddit) == 0

    def get_cluster_keys(self):
        schema = extract_pymongo_client_schema(
            self.client,
            database_names="m2ds_data_stream",
        )
        cluster_keys = set()
        for collection_schema in schema["m2ds_data_stream"].values():
            keys = collection_schema["object"].keys()
            for key in keys:
                if key.startswith("cluster"):
                    cluster_keys.add(key)

        self.cluster_keys = sorted(cluster_keys)

    def document_to_data(self, document):
        data = {
            "text": document["text"],
            "hashtags": document["hashtags"],
            "place": document["place_name"],
            "source": document["source"],
            "dt_created": document["dt_created"],
            "dt_storage": document["dt_storage"],
            "dt_download": self.datetime_now,
        }
        for cluster_key in self.cluster_keys:
            data[cluster_key] = document[cluster_key]
        return data

    def update_data(self):
        self.logger.info("Refreshing data")
        self.datetime_now = datetime.datetime.utcnow()

        dict_count = {
            "datetime": self.datetime_now,
            "twitter": 0,
            "reddit": 0,
            "total": 0,
        }

        new_documents_twitter = self.collection_twitter.find(
            {"dt_storage": {"$gt": self.last_query_time}}
        )
        new_documents_reddit = self.collection_reddit.find(
            {"dt_storage": {"$gt": self.last_query_time}}
        )

        for document in new_documents_twitter:
            data = self.document_to_data(document)
            self.data_memory_twitter.append(data)
            dict_count["twitter"] += 1
            dict_count["total"] += 1

        for document in new_documents_reddit:
            data = self.document_to_data(document)
            self.data_memory_reddit.append(data)
            dict_count["reddit"] += 1
            dict_count["total"] += 1

        self.count_memory.append(dict_count)
        self.last_query_time = self.datetime_now

    def export_viz_data(self, cluster_key="cluster"):
        df = (
            pd.DataFrame(self.data_memory_twitter + self.data_memory_reddit)
            .sort_values(by="dt_storage", ignore_index=True)
            .drop(columns=["dt_storage", "dt_download"])
        )

        pop_cluster = (
            df[cluster_key]
            .value_counts()
            .rename_axis(cluster_key)
            .reset_index(name="counts")
        )
        most_freq_clusters = pop_cluster[:3][cluster_key].tolist()
        most_freq_hashs = []
        valid = []
        for cl in most_freq_clusters:
            df_zoom = df[df[cluster_key] == cl]
            hash_cl = ", ".join(
                str(v) for v in df_zoom.hashtags if len(str(v)) > 1 and str(v) != "[]"
            )
            valid.append(len(hash_cl) > 1)
            most_freq_hashs.append(hash_cl)

        top_loc = (
            df.place.value_counts()[:10].rename_axis("loc").reset_index(name="counts")
        )

        df_count = pd.DataFrame(self.count_memory)

        return (
            df,
            top_loc,
            pop_cluster,
            df_count,
            most_freq_clusters,
            most_freq_hashs,
            valid,
        )
