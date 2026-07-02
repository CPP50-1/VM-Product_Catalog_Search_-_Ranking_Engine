import heapq
import math
import json

from engine.tokenize import tokenize
from engine.index import Index

def get_score(max_tokens: int, product_tokens: int, product: dict) -> float:
    """Gives score for a product based on number of tokens in search, stock and rank"""
    return ((product_tokens/max_tokens)*0.5 +
            product['stock']*0.2 +
            (1/ math.log2(product['sales_rank'] + 2))*0.3)


def search(query: str, top_k:int = 10):
    """returns a list of tuple (score, product), ordered by score and limited to top_k items"""
    tokens = tokenize(query)
    matches = {}
    searched_list= []
    index = Index()

    for token in tokens:
        list_product = index.get(token) or []
        for product in list_product:
            if matches.get(product):
                matches[product] += 1
            else: matches[product] = 1

    with open("catalog.json", "r") as f:
        data = json.load(f)
        for match_qty in matches:
            product = [element for element in data if element['id'] == match_qty]
            score = get_score(len(tokens), matches[match_qty], product[0])
            heapq.heappush(searched_list, (score, product))
            if len(searched_list) > top_k:
                heapq.heappop(searched_list)
    return sorted(searched_list, reverse=True)