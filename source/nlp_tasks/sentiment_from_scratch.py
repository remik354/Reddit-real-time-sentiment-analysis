import pickle
from source.nlp_tasks.sentiment_functions import clean_and_tokenize, sentence_representations

# load trained model
with open('source/materials/model_svd_ppmi.pkl', 'rb') as f:
    model_svd_ppmi = pickle.load(f)
print("The model has been loaded !")

# load vocabulary
with open('source/materials/vocabulary.pkl', 'rb') as v:
    vocabulary = pickle.load(v)
print("The vocabulary has been loaded !")

# load the SVD Matrix
with open('source/materials/M.pkl', 'rb') as v:
    M = pickle.load(v)
print("The matix has been loaded !")

def analyse_sentiment_scratch(comment_data):
    """
    Perform sentiment analysis on a comment using the model trained from scratch.
    """
    raw_text = clean_and_tokenize(comment_data['body'])
    representation = sentence_representations([raw_text], vocabulary, M)
    sentiment = model_svd_ppmi.predict(representation)
    comment_data["sentiment"] = float(sentiment[0])
    print(f'{comment_data["created_at"]}: A comment was treated, new sentiment update!')
    return comment_data
