import re

def tokenize(text: str):
    text = re.sub( r'[^\w\s]', ' ', text)
    text = re.sub( r'\W*\b\w{1,2}\b', ' ', text)
    text = re.sub(' +', ' ', text).strip()
    return re.split(' ', text)