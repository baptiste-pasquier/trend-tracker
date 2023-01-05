import json
import time

import pandas as pd
import streamlit as st
from kafka import KafkaConsumer
import plotly.express as px  # interactive charts

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

    df = pd.DataFrame({"hashtags": [],"cluster": [],"place_name": [],"source": []})
    fig_pop = st.bar_chart(df, x="cluster")
    fig_line =  st.line_chart(df,)
    fig_loc = st.bar_chart(df, x="cluster")
    for data in consumer:
        count_data += 1
        data = data.value
        new_data = {
            "hashtags": data["hashtags"],
            "cluster": data["cluster"],
            "place_name": data["place_name"],
            "source": data["source"]
        }
        list_data.append(new_data)
        df = pd.DataFrame(list_data)
        if data["cluster"] not in list_cluster:
            list_cluster.append(data["cluster"])

        with placeholder.container():
            st.header("General Data")
            kpi1, kpi2, fig_pop = st.columns(3)
            kpi1.metric(label="Total Nb Data", value=count_data )
            kpi2.metric(label="Nb Cluster", value=len(list_cluster))
            with fig_pop:
                st.markdown("Evolution of the population inside the clusters")
                fig_pop = px.histogram(data_frame=df, x="cluster")
                st.write(fig_pop)
            st.header("Top hashtags")          
            text = ", ".join(df['hashtags'].tolist())
            fig_line, fig_loc, = st.columns(2)
            with fig_line:
                st.markdown("Number of streamed data")
                fig_line =  px.line(df, x="year", y="lifeExp", color='country')
                st.write(fig_line)
            with fig_loc:
                st.markdown("Top Tweet Locations")
                fig_loc = px.histogram(data_frame=df, x="cluster")
                st.write(fig_loc)
            st.markdown("### Detailed Data view")
            st.dataframe(df.sort_values(by=["Cluster"]))
            time.sleep(0.5)


if __name__ == "__main__":
    main()
