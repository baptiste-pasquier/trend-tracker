import time
from kafka import kafkaConsumer
import streamlit as st
import plotly.express as px
from ingest_tweets import BOOTSTRAP_ENDPOINT,GROUP_ID
from cluster_data import CLUSTER_TOPIC


def main():
	st.set_page_config(
	    page_title="Real-Time Data Science Dashboard",
	    page_icon="✅",
	    layout="wide",
	)
	# dashboard title
	st.title("Real-Time / Live Data Science Dashboard")
	
	# creating a single-element container
	placeholder = st.empty()

	consumer = KafkaConsumer(CLUSTER_TOPIC, 
		bootstrap_servers=BOOTSTRAP_ENDPOINT,
		group_id = GROUP_ID,
		value_deserializer = lambda m: json.loads(m.decode('utf-8')))

	for data in consumer:
		data = data.value
		

if __name__ == "__main__":
	main()