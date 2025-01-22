import os
import tweepy
import time
import random
import json

from dotenv import load_dotenv
from datetime import datetime
from kafka import KafkaProducer

# Load environment variables with dotenv
load_dotenv()

# import login credetials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Connecting to tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Set the kafka broker
KAFKA_BROKER = "localhost:9092"
PRODUCER_TOPIC = "twitter_data"

# Set up the kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Words for the search
KEYWORDS = ["Trump"]

def get_random_tweet():
    try:
        # Choose a search word
        keyword = random.choice(KEYWORDS)
        print(f"Search for the keyword : {keyword}")
        
        # search in recent tweets
        response = client.search_recent_tweets(
            query=f"{keyword} -is:retweet lang:en",
            max_results=5,
            tweet_fields=["created_at", "text", "author_id"]
        )

        # check response
        if response.data:
            # print tweets
            for tweet in response.data:
                print(f"Content : {tweet.text} (Auteur : {tweet.author_id}, Date : {tweet.created_at})\n")
                tweet_data = {"author_id": tweet.author_id, 
                          "created_at": tweet.created_at.isoformat(), 
                          "content": tweet.text,
                }
                producer.send(PRODUCER_TOPIC, value=tweet_data)
        else:
            print("Nothing found with this request.\n")
    
    except tweepy.TooManyRequests as e:
        # Get the reset timer
        reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time()))
        wait_time = max(reset_time - int(time.time()), 1)
        reset_datetime = datetime.fromtimestamp(reset_time)
        print(f"{datetime.now()} - Exception: TooManyRequest. \nNew try at {reset_datetime}.")
        time.sleep(wait_time)

def main():
    while True:
        try:
            get_random_tweet()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")
            break

if __name__ == "__main__":
    main()
