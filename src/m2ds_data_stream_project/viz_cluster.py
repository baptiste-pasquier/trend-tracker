import matplotlib.pyplot as plt
import streamlit as st
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
