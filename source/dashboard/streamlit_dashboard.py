import streamlit as st
import pandas as pd
import json
import time
import plotly.express as px
from kafka import KafkaConsumer
import os

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
READING_TOPIC = "reddit_transformed"

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    READING_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True
)

# Streamlit Configuration
st.set_page_config(page_title="Real-Time Reddit Sentiment Dashboard", layout="wide")
st.title("Real-Time Reddit Sentiment Dashboard")

# Layout
col1, col2 = st.columns([3, 1])
col3, col4 = st.columns([3, 1])

# Display placeholders
with col1:
    # Add the subreddit filter above the comments table
    st.write("### Filter by Keyword")
    subreddit_filter = st.text_input(
        "Enter a key word to filter (leave blank for all):", ""
    )
    comment_table_placeholder = st.empty()

with col3:
    sentiment_chart_placeholder = st.empty()

with col4:
    bar_chart_placeholder = st.empty()

# Initialize data structures
comments_data = pd.DataFrame(columns=["Timestamp", "Username", "Content", "Category", "Topic Title", "Sentiment Score", "Subreddit"])

# Function to update Streamlit components
def update_streamlit_display(comments_data):
    # Filtrer les commentaires selon le filtre subreddit
    if subreddit_filter:
        filtered_data = comments_data[comments_data["Content"].str.contains(subreddit_filter, case=False, na=False)]
    else:
        filtered_data = comments_data

    # Mettre à jour l'affichage du tableau des commentaires
    with comment_table_placeholder.container():
        st.write("**Recent Comments**")
        st.dataframe(filtered_data.tail(5), use_container_width=True)

    # Mettre à jour le graphique des sentiments
    if not filtered_data.empty:
        with sentiment_chart_placeholder.container():
            filtered_data["Timestamp"] = pd.to_datetime(filtered_data["Timestamp"])
            sentiment_avg = (
                filtered_data.groupby([pd.Grouper(key="Timestamp", freq="1s"), "Category"])
                .agg({"Sentiment Score": "mean"})
                .reset_index()
            )
            fig = px.line(
                sentiment_avg,
                x="Timestamp",
                y="Sentiment Score",
                color="Category",
                title="Average Sentiment Evolution Over Time by Category",
                markers=True
            )
            try:
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass

    # Mettre à jour le graphique en barres
    if not filtered_data.empty:
        with bar_chart_placeholder.container():
            sentiment_dist = (
                filtered_data.groupby("Category")
                .agg({"Sentiment Score": "mean"})
                .reset_index()
            )
            fig = px.bar(
                sentiment_dist,
                x="Category",
                y="Sentiment Score",
                title="Average Sentiment Score by Category",
                labels={"Sentiment Score": "Average Sentiment"}
            )
            try:
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass


# Function to read the latest data from archives.txt
def read_archives_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
        # Convert lines to a list of dictionaries (comments)
        return [json.loads(line) for line in lines]
    else:
        return []

# Load initial data from archives.txt into the DataFrame
initial_comments = read_archives_file("data/archives.txt")
if initial_comments:
    comments_data = pd.DataFrame(initial_comments)

# Main loop: Periodically read Kafka messages and update Streamlit display
st.write("Listening for incoming comments...")

while True:
    # Read a new message from Kafka
    for message in consumer:
        comment = message.value

        # Extract relevant fields
        timestamp = comment.get("created_at")
        username = comment.get("author")
        content = comment.get("body")
        topic = comment.get("topic_title")
        category = comment.get("category")  # Topic the comment belongs to
        sentiment = comment.get("sentiment")  # Sentiment score
        subreddit = comment.get("subreddit")  # Subreddit name

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

        comments_data = pd.concat(
            [comments_data, pd.DataFrame([new_comment])],
            ignore_index=True
        )

        # Update the Streamlit display
        update_streamlit_display(comments_data)

    # Add a small delay to prevent overloading Streamlit
    time.sleep(0.5)
