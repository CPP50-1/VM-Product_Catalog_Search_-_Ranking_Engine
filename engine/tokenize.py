import re

def tokenize(text):
    text = re.sub( r'[^\w\s]', ' ', text)
    text = re.sub( r'\W*\b\w{1,3}\b', ' ', text)
    text = re.sub(' +', ' ', text).strip()
    result = re.split('[ ,.?]', text)
    return result