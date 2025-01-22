import streamlit as st
import pandas as pd
from kafka import KafkaConsumer
import json
import time
import plotly.express as px

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

# Display placeholders
with col1:
    comment_table_placeholder = st.empty()
    sentiment_chart_placeholder = st.empty()

with col2:
    topic_pie_chart_placeholder = st.empty()

# Initialize data structures
comments_data = pd.DataFrame(columns=["Timestamp", "Username", "Content", "Category", "Topic Title", "Sentiment Score"])

# Function to update Streamlit components
def update_streamlit_display(comments_data):
    # Update table display (limit to 10 recent comments)
    with comment_table_placeholder.container():
        st.write("**Recent Comments**")
        st.dataframe(comments_data.tail(10), use_container_width=True)

    # Update line chart of sentiment evolution
    if not comments_data.empty:
        with sentiment_chart_placeholder.container():
            st.write("**Sentiment Evolution by Category**")
            
            # Convert Timestamp to datetime for proper plotting
            comments_data["Timestamp"] = pd.to_datetime(comments_data["Timestamp"])
            
            # Group data by category and timestamp, then calculate the mean sentiment score
            sentiment_avg = (
                comments_data.groupby([pd.Grouper(key="Timestamp", freq="10s"), "Category"])
                .agg({"Sentiment Score": "mean"})
                .reset_index()
            )
            
            # Plot the line chart using the aggregated data
            fig = px.line(
                sentiment_avg,
                x="Timestamp",
                y="Sentiment Score",
                color="Category",
                title="Average Sentiment Evolution Over Time by Category",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

    # # Update pie chart of topic proportions
    # if not comments_data.empty:
    #     with topic_pie_chart_placeholder.container():
    #         st.write("**Topic Category Proportions**")
    #         topic_counts = comments_data["Category"].value_counts()
    #         fig = px.pie(
    #             names=topic_counts.index,
    #             values=topic_counts.values,
    #             title="Proportion of Topic Categories in Comments"
    #         )
    #         st.plotly_chart(fig, use_container_width=True, key="topic_pie_chart_unique")

# Main loop: Listen to Kafka messages and update Streamlit display
st.write("Listening for incoming comments...")

while True:
    for message in consumer:
        comment = message.value

        # Extract relevant fields
        timestamp = comment.get("created_at")
        username = comment.get("author")
        content = comment.get("body")
        topic = comment.get("topic_title")
        category = comment.get("category")  # Topic the comment belongs to
        sentiment = comment.get("sentiment")  # Sentiment score

        # Update data
        new_comment = {
            "Timestamp": timestamp,
            "Username": username,
            "Content": content,
            "Category": category,
            "Topic Title": topic,
            "Sentiment Score": sentiment,
        }

        comments_data = pd.concat(
            [comments_data, pd.DataFrame([new_comment])],
            ignore_index=True
        )

        # Update the Streamlit display
        update_streamlit_display(comments_data)

        # Add a small delay to prevent overloading Streamlit
        time.sleep(0.1)
