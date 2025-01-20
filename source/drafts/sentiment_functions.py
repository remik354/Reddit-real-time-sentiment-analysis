import re
from nltk.tokenize import word_tokenize

# Clean and tokenize the sentence 
def clean_and_tokenize(text):
    """
    Cleaning a document with:
        - Lowercase
        - Removing all that is not a number or a letter
        - Removing all urls
    And separate the document into words by simply splitting at spaces
    Params:
        text (string): a sentence or a document
    Returns:
        tokens (list of strings): the list of tokens (word units) forming the document
    """
    text = text.lower()
    REMOVE_PUNCT = re.compile(r"@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+")
    text = REMOVE_PUNCT.sub(" ", text)
    return word_tokenize(text, language='english')

