################################################################
# reduce the warnings
import os
import logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
################################################################

# topic classification
from transformers import pipeline

# Load model
topic_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Categories for topic classification
categories = [
    "Politics",
    "Technology",
    "Entertainment",
    "Finance",
    "Health",
]

def classify_topic(comment_data):
    """
    Classify the topic of a comment based on its topic title.
    """
    category = topic_classifier(comment_data["topic_title"], candidate_labels=categories)
    comment_data["category"] = category["labels"][0]
    return comment_data
