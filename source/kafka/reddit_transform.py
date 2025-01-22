import time
import json
import random
from kafka import KafkaProducer, KafkaConsumer
from transformers import pipeline

# Set the kafka broker
KAFKA_BROKER = "localhost:9092"
WRITING_TOPIC = "reddit_transformed" 
READING_TOPIC = "reddit_topic" 

# Set up the kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
consumer = KafkaConsumer(
    READING_TOPIC, 
    bootstrap_servers=KAFKA_BROKER, 
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# load model for topic classification
topic_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# to be chosen ?
categories = ["News and Politics",
              "Technology and Science",
              "Entertainment and Pop Culture", 
              "Business and Finance",
              "Health and Well-being",
              "Everyday Life and Hobbies",
]

# load model for sentiment analysis
# to be chosen ? 
sentiment_classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Topic classification
def classify_topic(comment_data):
    # title topic classification (what is the context of the comment ?)
    category = topic_classifier(comment_data["topic_title"], candidate_labels=categories)
    comment_data["category"] = category["labels"][0]
    return comment_data

# Sentiment analysis
def classify_sentiment(comment_data): #, model):
    result = sentiment_classifier(comment_data['body'])
    sentiment = result[0]['score']
    comment_data["sentiment"] = sentiment
    print(f'{comment_data["created_at"]}: A comment was treated, new sentiment update !')
    return comment_data

def transform_data(comment_data):
    comment_data = classify_topic(comment_data)
    comment_data = classify_sentiment(comment_data)
    producer.send(WRITING_TOPIC, value=comment_data)
                
while True:
    print("\n Listening to comments...")
    for message in consumer:
        comment_data = message.value
        transform_data(comment_data)
    print("Done ! A wave of coments has been treated :) \n")
