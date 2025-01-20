import streamlit as st
import pandas as pd
from kafka import KafkaConsumer
import json
import time

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
READING_TOPIC = "twitter_data"

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    READING_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True
)

# Streamlit Configuration
st.set_page_config(page_title="Real-Time Tweet Sentiment Dashboard", layout="wide")
st.title("Real-Time Tweet Sentiment Dashboard")

# Layout
col1, col2 = st.columns([3, 1])

# Display placeholders
with col1:
    tweet_table_placeholder = st.empty()

with col2:
    sentiment_chart_placeholder = st.empty()

# Initialize data structures
tweets_data = pd.DataFrame(columns=["Timestamp", "Username", "Content", "Sentiment"])
sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}


# Helper function to update sentiment counts
def update_sentiment_counts(sentiment):
    if sentiment in sentiment_counts:
        sentiment_counts[sentiment] += 1
    else:
        sentiment_counts[sentiment] = 1


# Function to update the Streamlit components
def update_streamlit_display():
    # Update table display (limit to 10 recent tweets)
    with tweet_table_placeholder.container():
        st.write("**Recent Tweets**")
        st.table(tweets_data.tail(10))

    # Update sentiment distribution chart
    with sentiment_chart_placeholder.container():
        sentiment_df = pd.DataFrame(
            list(sentiment_counts.items()), columns=["Sentiment", "Count"]
        )
        st.write("**Sentiment Distribution**")
        st.bar_chart(sentiment_df.set_index("Sentiment"))


# Main loop: Listen to Kafka messages and update Streamlit display
st.write("Listening for incoming tweets...")

# Streamlit's interactive approach to prevent blocking
for message in consumer:
    tweet = message.value

    # Extract relevant fields
    timestamp = tweet.get("created_at")
    username = tweet.get("author_id")  # You can replace this with the actual username if you fetch it
    content = tweet.get("content")
    sentiment = tweet.get("sentiment", "Neutral")  # Default to Neutral if missing

    # Update sentiment counts and data
    update_sentiment_counts(sentiment)
    tweets_data = pd.concat(
        [
            tweets_data,
            pd.DataFrame.from_records(
                [
                    {
                        "Timestamp": timestamp,
                        "Username": username,
                        "Content": content,
                        "Sentiment": sentiment,
                    }
                ]
            ),
        ]
    )

    # Update the Streamlit display
    update_streamlit_display()

    # Add a small delay to prevent overloading Streamlit
    time.sleep(0.5)
