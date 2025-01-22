import os
import praw
import time
import json

from dotenv import load_dotenv
from datetime import datetime
from kafka import KafkaProducer

# Load environment variables with dotenv
load_dotenv()

# Initialize Reddit API via env variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# Set the kafka broker
KAFKA_BROKER = "localhost:9092"
WRITING_TOPIC = "reddit_topic" 

# Set up the kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_comments(subreddit_list):
    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name)
        for comment in subreddit.stream.comments(skip_existing=True):
            try:
                submission = comment.submission
                topic_title = f"{subreddit.display_name}: {submission.title}"
            except Exception as e:
                continue

            submission = comment.submission
            comment_data = {
                # "id": comment.id,
                # "name": comment.name,
                "author": comment.author.name if comment.author else "Deleted",
                "body": comment.body[:300],
                "subreddit": comment.subreddit.display_name.lower(),
                # "upvotes": comment.ups,
                # "downvotes": comment.downs,
                "created_at": datetime.fromtimestamp(comment.created_utc).isoformat(),
                "timestamp": comment.created_utc,
                # "permalink": comment.permalink,
                "topic_title": topic_title,  # Subreddit title + Topic title
            }

            print(f'New comment ! \n{comment_data["created_at"]}: Author - {comment_data["author"]} / Subreddit - {comment.subreddit.display_name.lower()}\n{comment.body}\n')
            producer.send(WRITING_TOPIC, value=comment_data)


def main():
    while True:
        try:
            # To get from streamlit
            subreddit_list = ['all']
            fetch_comments(subreddit_list)
            # time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")
            break

if __name__ == "__main__":
    main()
