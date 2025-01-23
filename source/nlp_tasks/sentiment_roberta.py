################################################################
# reduce the warnings
import os
import logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
################################################################

# sentiment analysis
from transformers import pipeline

# Load model for sentiment analysis
sentiment_classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def analyse_sentiment_pretrained(comment_data):
    """
    Perform sentiment analysis on a comment using the pretrained model.
    """
    result = sentiment_classifier(comment_data['body'])
    sentiment = result[0]['score']
    comment_data["sentiment"] = sentiment
    print(f'{comment_data["created_at"]}: A comment was treated, new sentiment update!')
    return comment_data
