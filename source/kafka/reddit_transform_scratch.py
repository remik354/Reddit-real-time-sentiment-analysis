import json
from kafka import KafkaProducer, KafkaConsumer
from source.nlp_tasks.topic_bart import classify_topic
from source.nlp_tasks.sentiment_from_scratch import analyse_sentiment_scratch

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
WRITING_TOPIC = "reddit_transformed" 
READING_TOPIC = "reddit_topic" 

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Set up Kafka consumer
consumer = KafkaConsumer(
    READING_TOPIC, 
    bootstrap_servers=KAFKA_BROKER, 
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# apply topic detection and sentiment analysis
def transform_data(comment_data):
    """
    Apply topic classification and sentiment analysis to the comment data,
    then send it to the producer.
    """
    comment_data = classify_topic(comment_data)
    comment_data = analyse_sentiment_scratch(comment_data)   
    producer.send(WRITING_TOPIC, value=comment_data)

# Main loop for consuming, transforming, and producing comments
if __name__ == "__main__":
    print("\nListening to comments...")
    for message in consumer:
        comment_data = message.value
        transform_data(comment_data)
    print("Done! A wave of comments has been treated :) \n")
