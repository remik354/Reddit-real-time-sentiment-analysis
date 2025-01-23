import re
import numpy as np
from nltk.tokenize import word_tokenize

# Clean and tokenize the sentence 
def clean_and_tokenize(text):
    """
    Cleaning a document with:
        - Lowercase
        - Removing all that is not a number or a letter
        - Removing all urls
    And separate the document into words by simply splitting at spaces
    """
    text = text.lower()
    REMOVE_PUNCT = re.compile(r"@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+")
    text = REMOVE_PUNCT.sub(" ", text)
    return word_tokenize(text, language='english')

# give the sentence representation to the sentence
def sentence_representations(texts, vocabulary, embeddings, np_func=np.mean):
    """
    Represent the sentences as a combination of the vector of its words.
    """
    representations = np.zeros((len(texts), embeddings.shape[1]))
    for i, sentence in enumerate(texts):
        word_vectors = []

        for word in sentence:
            if word in vocabulary.keys():
                word_idx = vocabulary[word]
                word_vectors.append(embeddings[word_idx])

        if word_vectors:
            word_vectors = np.array(word_vectors)
            representations[i] = np_func(word_vectors, axis=0)
        else:
            representations[i] = np.zeros(embeddings.shape[1])
    return representations