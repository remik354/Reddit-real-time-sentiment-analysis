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

def fetch_comments(subreddit_list, limit=10):
    """
    Fetch comments from a list of subreddits and send them to the Kafka broker.
    """
    # keep the count to get limit comments each second
    comment_count = 0
    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name)
        if comment_count > limit:
                return
        for comment in subreddit.stream.comments(skip_existing=True):
            if comment_count > limit:
                return
            try:
                submission = comment.submission
                topic_title = f"{subreddit.display_name}: {submission.title}"
            except Exception as e:
                continue

            # Only keep the first 250 characters (for computational cost reasons)
            text = comment.body[:250]
            
            comment_data = {
                "author": comment.author.name if comment.author else "Deleted",
                "body": text,
                "subreddit": comment.subreddit.display_name.lower(),
                "created_at": datetime.fromtimestamp(comment.created_utc).isoformat(),
                "timestamp": comment.created_utc,
                "topic_title": topic_title,  # Subreddit title ^ Topic title
            }

            # print a notification and send the comment to the kafka broker
            print(f'New comment ! \n{comment_data["created_at"]}: Author - {comment_data["author"]} / Subreddit - {comment.subreddit.display_name.lower()}\n{text}\n')
            producer.send(WRITING_TOPIC, value=comment_data)

            # update the count
            comment_count += 1

def main():
    while True:
        try:
            # Fetch comments from the 'all' subreddit (it is by itself a list of all subreddits)
            subreddit_list = ['all']
            fetch_comments(subreddit_list)
        except KeyboardInterrupt:
            print("Exit")
            break

if __name__ == "__main__":
    main()
