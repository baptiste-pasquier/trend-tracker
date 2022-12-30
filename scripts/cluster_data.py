from river import feature_extraction, metrics, cluster
from kafka import KafkaProducer, KafkaConsumer
import json
import time

from ingest_tweets import BOOTSTRAP_ENDPOINT
from tsf_data import CLEAN_TOPIC, GROUP_ID

CLUSTER_TOPIC = "cluster_texts"


def main():
	
	producer = KafkaProducer(
		bootstrap_servers=BOOTSTRAP_ENDPOINT,
		value_serializer=lambda m: json.dumps(m).encode("utf8"))
	#Call a Consumer to retrieve the raw tweets
	
	consumer = KafkaConsumer(CLEAN_TOPIC, 
		bootstrap_servers=BOOTSTRAP_ENDPOINT,
		group_id = GROUP_ID,
		value_deserializer = lambda m: json.loads(m.decode('utf-8')))
	
	#tfidf = feature_extraction.TFIDF()
	#adj_rand_score = metrics.AdjusterRand()
	#silhouette_score = metrics.Silhouette()

	model = feature_extraction.BagOfWords(ngram_range=(1,2))
	model |= cluster.TextClust(real_time_fading = False, 
							fading_factor=0.001, 
							tgap=100, 
							auto_r=True)

	for data in consumer:
		data = data.value
		print(data['text'],"\n\n")
		data['cluster'] = model.predict_one(data["text"])
		model = model.learn_one(data["text"])
		print(data['cluster'])
		producer.send(CLUSTER_TOPIC,data)

	

if __name__ == "__main__":
	main()