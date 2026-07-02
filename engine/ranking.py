import heapq
import math

from engine.tokenize import tokenize

def get_score(max_tokens: int, product: dict) -> float:
    return ((product['match']/max_tokens)*0.5 +
            product['product']['stock']*0.2 +
            (1/ math.log2(product['product']['rank'] + 2))*0.3)


def search(query: str, top_k:int = 10):
    tokens = tokenize(query)
    results = {}
    searched_list= []

    for token in tokens:
        list_product = [] # todo use index to get a product list for each token
        for product in list_product:
            if results.get(product['id']):
                results[product['id']]['match'] += 1
            else: results[product['id']] = {'match': 1, 'product': product}

    for result in results:
        score = get_score(len(tokens), result)
        heapq.heappush(searched_list, (score, result['product']))
        if len(searched_list) > top_k:
            heapq.heappop(searched_list)
    return searched_list