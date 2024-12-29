# Necessary imports
import json
import os
import time
import tweepy
from dotenv import load_dotenv
from kafka import KafkaProducer
import tweepy.cursor

# Load environment variables with dotenv
load_dotenv()

# Load the credentials
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Set the kafka broker
KAFKA_BROKER = "localhost:9092"
PRODUCER_TOPIC = "twitter_data"

# Set up the kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Setup Tweepy API
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

cursor=tweepy.Cursor(api.search_tweets, q="music", lang="en", tweet_mode="extended").items(1)

for tweet in cursor:
    hashtags=tweet.entities['hashtags']

    hashtext = list()
    for j in range(0, len(hashtags)):
        hashtext.append(hashtags[j]['text'])

    cur_data = {
        "username": tweet.user.name,
        "tweet": tweet.full_text
    }

    print(cur_data)




# class StreamListener(tweepy.StreamingClient):
#     def on_tweet(self, tweet):
#         try:
#             tweet_data = {
#                 'user': tweet.author_id,
#                 'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
#                 'text': tweet.text,
#             }
#             producer.send(PRODUCER_TOPIC, value=tweet_data)
#             print(f"Tweet sent to Kafka: {tweet_data['text']}")
#         except Exception as e:
#             print(f"Error processing tweet: {e}")

#     def on_error(self, status_code):
#         if status_code == 420:
#             return False
#         print(f"Error: {status_code}")


# if __name__ == "__main__":
#     stream_listener = StreamListener(BEARER_TOKEN)
#     try:
#         stream_listener.sample()
        
#     except KeyboardInterrupt:
#         print("Streaming stopped.")

# # Stream encountered HTTP error: 403
# # HTTP error response text: {"client_id":"29825133","detail":"When authenticating requests to the Twitter API v2 endpoints, you must use keys and tokens from a Twitter developer App that is attached to a Project. You can create a project via the developer portal.","registration_url":"https://developer.twitter.com/en/docs/projects/overview","title":"Client Forbidden","required_enrollment":"Appropriate Level of API Access","reason":"client-not-enrolled","type":"https://api.twitter.com/2/problems/client-forbidden"}
