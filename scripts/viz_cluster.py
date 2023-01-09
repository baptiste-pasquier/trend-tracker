import os
import time

import plotly.express as px
import streamlit as st

from m2ds_data_stream_project.tools import load_config, load_config_in_environment
from m2ds_data_stream_project.viz_cluster import DataViz, make_wordCloud


def main():
    # Load config
    if os.path.isfile("secret_config.yml"):
        load_config_in_environment("secret_config.yml")
    config = load_config("config.yml")

    # Initialize DataViz
    dataviz = DataViz(os.environ["MONGODB_CONNECTION_STRING"])
    dataviz.update_data()

    st.set_page_config(
        page_title="Real-Time Dashboard",
        page_icon="✅",
        layout="wide",
    )
    # dashboard title
    st.title("Real-Time / Live Data News Dashboard")

    placeholder = st.empty()

    while True:
        dataviz.update_data()

        (
            df_data,
            top_loc,
            pop_cluster,
            df_count,
            most_freq_clusters,
            most_freq_hashs,
            valid,
        ) = dataviz.export_viz_data()

        nb_cluster = len(set(df_data.cluster))
        nb_data = df_count["total"].sum()

        with placeholder.container():
            kpi_nb_cl, kpi_nb_t, fig_loc = st.columns(3)
            kpi_nb_cl.metric(label="Nb Cluster", value=nb_cluster)
            kpi_nb_t.metric(label="Nb Data", value=nb_data)
            with fig_loc:
                st.markdown("Evolution of the top locations (tweet only)")
                st.table(top_loc)

            st.markdown("Evolution of the population inside the clusters")
            fig_pop = px.bar(pop_cluster, x="cluster", y="counts")
            st.write(fig_pop)
            st.markdown("Evolution of the data sources")
            fig_src = px.line(df_count.loc[1:], x="datetime", y=["reddit", "twitter"])
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
                    df_zoom = df_data[df_data["cluster"] == id_cluster]
                    st.dataframe(df_zoom)
                with df_2:
                    id_cluster = most_freq_clusters[1]
                    st.markdown(f"Cluster {id_cluster}")
                    df_zoom = df_data[df_data["cluster"] == id_cluster]
                    st.dataframe(df_zoom)
                with df_3:
                    id_cluster = most_freq_clusters[2]
                    st.markdown(f"Cluster {id_cluster}")
                    df_zoom = df_data[df_data["cluster"] == id_cluster]
                    st.dataframe(df_zoom)
        time.sleep(config["refresh_time"])


if __name__ == "__main__":
    main()
