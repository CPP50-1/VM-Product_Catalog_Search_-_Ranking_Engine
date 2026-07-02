import heapq
import math

from engine.tokenize import tokenize
from engine.index import Index

def get_score(max_tokens: int, product: dict) -> float:
    return ((product['match']/max_tokens)*0.5 +
            product['product']['stock']*0.2 +
            (1/ math.log2(product['product']['rank'] + 2))*0.3)


def search(query: str, top_k:int = 10):
    tokens = tokenize(query)
    results = {}
    searched_list= []
    index = Index()

    for token in tokens:
        list_product = index[token]
        for product in list_product:
            if results.get(product):
                results[product]['match'] += 1
            else: results[product] = {'match': 1}

    for result in results:
        # score = get_score(len(tokens), result)
        heapq.heappush(searched_list, (1, result))
        if len(searched_list) > top_k:
            heapq.heappop(searched_list)
    return searched_list
print(search('bluetooth',1000))