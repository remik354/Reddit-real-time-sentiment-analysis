import time
import pandas as pd
import pickle
from kafka import KafkaConsumer
from sentiment_functions import clean_and_tokenize

dataframe = pd.read_csv('data/1000_tweets_sympas.csv')

# load trained model
with open('source/materials/model_svd_ppmi.pkl', 'rb') as f:
    model_svd_ppmi = pickle.load(f)
print("The model has been loaded !")

# load vocabulary model
with open('source/materials/vocabulary.pkl', 'rb') as v:
    vocabulary = pickle.load(v)
print("The vocabulary has been loaded !")

def analyse_sentiment(tweet):
    raw_sentence = clean_and_tokenize(tweet['text'])
    sentence = [[word for word in raw_sentence if word in vocabulary.keys()]]
    print(sentence)

    prediction = model_svd_ppmi.predict(sentence)
    print(f"The sentiment of this tweet is {prediction}")
    return None

analyse_sentiment(dataframe.iloc[0])
            
# while True:
#     print("\n Listening to tweets...")
#     for message in consumer:
#         tweet = message.value
#         analyse_sentiment(tweet)
#     print("Done ! All the tweets have been treated :) \n")
#     time.sleep(10)
