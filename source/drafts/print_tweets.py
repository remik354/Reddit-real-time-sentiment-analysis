import tweepy
from tweepy import StreamingClient, StreamRule
import os
from dotenv import load_dotenv
load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')

class TweetPrinterV2(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        print(f"{tweet.id} {tweet.created_at} ({tweet.author_id}): {tweet.text}")
        print("-"*50)

printer = TweetPrinterV2(bearer_token)

# add new rules    
rule = StreamRule(value="Python")
printer.add_rules(rule)

printer.filter()