import json
from kafka import KafkaConsumer

# Set the kafka broker
KAFKA_BROKER = "localhost:9092"
READING_TOPIC = "reddit_transformed"

# Set up the kafka consumer
consumer = KafkaConsumer(
    READING_TOPIC, 
    bootstrap_servers=KAFKA_BROKER, 
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Write the new comment in the archive.txt file
with open("data/archives.txt", "w") as f:
    for message in consumer:
        comment = message.value
        
        # Extract relevant fields
        timestamp = comment.get("created_at")
        username = comment.get("author")
        content = comment.get("body")
        topic = comment.get("topic_title")
        category = comment.get("category")      # Topic the comment belongs to
        sentiment = comment.get("sentiment")    # Sentiment score
        subreddit = comment.get("subreddit")    # Subreddit name

        # Update data
        new_comment = {
            "Timestamp": timestamp,
            "Username": username,
            "Content": content,
            "Category": category,
            "Topic Title": topic,
            "Sentiment Score": sentiment,
            "Subreddit": subreddit,
        }

        f.write(json.dumps(new_comment) + "\n")
        print("A comment was written in the archive file")