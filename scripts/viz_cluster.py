import json

import pandas as pd
import plotly.express as px
import streamlit as st
from kafka import KafkaConsumer

from m2ds_data_stream_project.tools import load_config
from m2ds_data_stream_project.viz_cluster import make_wordCloud


def main():
    # Load config
    config = load_config("config.yml")

    st.set_page_config(
        page_title="Real-Time Dashboard",
        page_icon="✅",
        layout="wide",
    )
    # dashboard title
    st.title("Real-Time / Live Data News Dashboard")

    consumer = KafkaConsumer(
        config["cluster_topic"],
        bootstrap_servers=config["bootstrap_endpoint"],
        group_id=config["group_id"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    list_data = []
    dict_source = [{"index": 0, "reddit": 0, "twitter": 0}]
    placeholder = st.empty()
    for nb_data, data in enumerate(consumer):
        data = data.value
        new_data = {
            "text": data["text"],
            "hashtags": data["hashtags"],
            "cluster": data["cluster"],
            "place": data["place_name"],
            "source": data["source"],
        }
        list_data.append(new_data)
        df = pd.DataFrame.from_records(list_data)

        nb_cl = len(set(df.cluster))

        pop_cluster = (
            df.cluster.value_counts().rename_axis("cluster").reset_index(name="counts")
        )
        most_freq_clusters = pop_cluster[:3].cluster.tolist()
        most_freq_hashs = []
        valid = []
        for cl in most_freq_clusters:
            df_zoom = df[df["cluster"] == cl]
            hash_cl = ", ".join(
                str(v) for v in df_zoom.hashtags if len(str(v)) > 1 and str(v) != "[]"
            )
            valid.append(len(hash_cl) > 1)
            most_freq_hashs.append(hash_cl)
        top_loc = (
            df.place.value_counts()[:10].rename_axis("loc").reset_index(name="counts")
        )
        if new_data["source"] == "twitter":
            dict_source.append(
                {
                    "index": nb_data,
                    "twitter": dict_source[-1]["twitter"] + 1,
                    "reddit": dict_source[-1]["reddit"],
                }
            )
        else:
            dict_source.append(
                {
                    "index": nb_data,
                    "twitter": dict_source[-1]["twitter"],
                    "reddit": dict_source[-1]["reddit"] + 1,
                }
            )
        df_source = pd.DataFrame.from_records(dict_source)
        with placeholder.container():
            kpi_nb_cl, kpi_nb_t, fig_loc = st.columns(3)
            kpi_nb_cl.metric(label="Nb Cluster", value=nb_cl)
            kpi_nb_t.metric(label="Nb Data", value=nb_data)
            with fig_loc:
                st.markdown("Evolution of the top locations (tweet only)")
                st.table(top_loc)

            st.markdown("Evolution of the population inside the clusters")
            fig_pop = px.bar(pop_cluster, x="cluster", y="counts")
            st.write(fig_pop)
            st.markdown("Evolution of the data sources")
            fig_src = px.line(df_source, x="index", y=["reddit", "twitter"])
            st.write(fig_src)
            if (len(most_freq_hashs) >= 3) and (min(valid) is True):
                wc1, wc2, wc3 = st.columns(3)
                with wc1:
                    words, id_cluster = most_freq_hashs[0], most_freq_clusters[0]
                    make_wordCloud(words, id_cluster)
                with wc2:
                    words, id_cluster = most_freq_hashs[1], most_freq_clusters[1]
                    make_wordCloud(words, id_cluster)
                with wc3:
                    words, id_cluster = most_freq_hashs[2], most_freq_clusters[2]
                    make_wordCloud(words, id_cluster)
            if len(most_freq_clusters) == 3:
                st.markdown("### Detailed Data view")
                df_1, df_2, df_3 = st.columns(3)
                with df_1:
                    id_cluster = most_freq_clusters[0]
                    st.markdown(f"Cluster {id_cluster}")
                    df_zoom = df[df["cluster"] == id_cluster]
                    st.dataframe(df_zoom)
                with df_2:
                    id_cluster = most_freq_clusters[1]
                    st.markdown(f"Cluster {id_cluster}")
                    df_zoom = df[df["cluster"] == id_cluster]
                    st.dataframe(df_zoom)
                with df_3:
                    id_cluster = most_freq_clusters[2]
                    st.markdown(f"Cluster {id_cluster}")
                    df_zoom = df[df["cluster"] == id_cluster]
                    st.dataframe(df_zoom)


if __name__ == "__main__":
    main()
