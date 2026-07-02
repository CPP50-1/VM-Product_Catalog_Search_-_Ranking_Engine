import re

def tokenize(text: str):
    '''Returns a list of tokens from the given text, ignoring punctuation and 2- letters words'''
    # removes non-letters
    text = re.sub( r'[^\w\s]', ' ', text)
    # removes words that are 2 or less letters
    text = re.sub( r'\W*\b\w{1,2}\b', ' ', text)
    # removes multiple spaces
    text = re.sub(' +', ' ', text).strip()
    return re.split(' ', text)