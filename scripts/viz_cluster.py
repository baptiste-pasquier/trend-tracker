import json
import time

import pandas as pd
import streamlit as st
from kafka import KafkaConsumer

from m2ds_data_stream_project.tools import load_config


def main():
    # Load config
    config = load_config("config.yml")

    st.set_page_config(
        page_title="Real-Time News Dashboard",
        page_icon="✅",
        layout="wide",
    )
    # dashboard title
    st.title("Real-Time / Live Data News Dashboard")

    # creating a single-element container
    placeholder = st.empty()

    consumer = KafkaConsumer(
        config["cluster_topic"],
        bootstrap_servers=config["bootstrap_endpoint"],
        group_id=config["group_id"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    list_data = []
    count_data = 0
    list_cluster = []
    # creating a single-element container
    placeholder = st.empty()
    for data in consumer:
        count_data += 1
        data = data.value
        new_data = {
            "Text": data["text"],
            "Hashtags": data["hashtags"],
            "Cluster": data["cluster"],
            "Place": data["place_name"],
        }
        list_data.append(new_data)
        df = pd.DataFrame(list_data)
        if data["cluster"] not in list_cluster:
            list_cluster.append(data["cluster"])

        with placeholder.container():
            kpi1, kpi2 = st.columns(2)
            kpi1.metric(label="Nb Cluster", value=len(list_cluster))
            kpi2.metric(label="Total Nb Data", value=count_data)
            st.markdown("### Detailed Data view")
            st.dataframe(df.sort_values(by=["Cluster"]))
            time.sleep(0.5)


if __name__ == "__main__":
    main()