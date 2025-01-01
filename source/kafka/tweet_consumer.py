import time
import json
import pickle
from kafka import KafkaConsumer
from sentiment_analysis.sentiment_functions import clean_and_tokenize

# Set the kafka broker
KAFKA_BROKER = "localhost:9092"
READING_TOPIC = "twitter_data"

consumer = KafkaConsumer(
    READING_TOPIC, 
    bootstrap_servers=KAFKA_BROKER, 
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# load trained model
with open('../materials/model_svd_ppmi.pkl', 'rb') as f:
    model_svd_ppmi = pickle.load(f)
print("The model has been loaded !")

# load vocabulary model
with open('../materials/vocabulary.pkl', 'rb') as v:
    vocabulary = pickle.load(v)
print("The vocabulary has been loaded !")

def analyse_sentiment(tweet):
    raw_sentence = clean_and_tokenize(tweet['content'])
    sentence = [word for word in raw_sentence if word in vocabulary.keys()]
    print(sentence)

    prediction = model_svd_ppmi.predict(sentence)
    print(f"The sentiment of this tweet is {prediction}")
    return None
            
while True:
    print("\n Listening to tweets...")
    for message in consumer:
        tweet = message.value
        analyse_sentiment(tweet)
    print("Done ! All the tweets have been treated :) \n")
    time.sleep(10)
