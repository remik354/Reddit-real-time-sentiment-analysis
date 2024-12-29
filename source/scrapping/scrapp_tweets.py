import asyncio
import csv
import json
import os

from datetime import datetime
from dotenv import load_dotenv
from kafka import KafkaProducer
from random import randint
from twikit import Client, TooManyRequests

# Load environment variables with dotenv
load_dotenv()

# import login credetials
USERNAME = os.getenv("USERNAME")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Set the kafka broker
KAFKA_BROKER = "localhost:9092"
PRODUCER_TOPIC = "twitter_data"

# Set up the kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Definition of the query and the number of tweets to get (get rid of this later)
MINIMUM_TWEETS = 5
QUERY = 'Donald Trump'

# authenticate 
client = Client(language='en-US')

async def main():
    await client.login(
        auth_info_1=USERNAME ,
        auth_info_2=EMAIL,
        password=PASSWORD
    )

    tweets = None
    tweet_count = 0

    while tweet_count < MINIMUM_TWEETS:
        try:
            if tweets is None:
                print(f'{datetime.now()} - Getting tweets...')
                tweets = await client.search_tweet(QUERY, count=1, product='Top')
            else:
                wait_time = randint(2, 15)
                print(f'{datetime.now()} - Waiting {wait_time} seconds before fetching more tweets...')
                await asyncio.sleep(wait_time)
                tweets = await tweets.next()

        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            print(f'{datetime.now()} - Exception: TooManyRequests... Waiting until {rate_limit_reset} ({wait_time:.2f} seconds)')
            await asyncio.sleep(wait_time)
            continue

        if not tweets:
            print(f'{datetime.now()} -No more tweets to scrap')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = {"tweet_count": tweet_count, 
                          "username": tweet.user.name, 
                          "created_at": tweet.created_at, 
                          "retweet_count": tweet.retweet_count, 
                          "likes": tweet.retweet_count , 
                          "content": tweet.text
            }

            with open('../../data/tweets.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)
            producer.send(PRODUCER_TOPIC, value=tweet_data)
            
        print(f'{datetime.now()} -Got {tweet_count} tweets')

    print(f'{datetime.now()} -Done ! Got {tweet_count} tweets')

# create a csv:
with open('../../data/tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['No.', 'Username', 'Created At', 'Retweets', 'Likes', 'Text'])

asyncio.run(main())
