import heapq
import math

from engine.index import Index

def get_score(max_tokens: int, product_tokens: int, product: dict) -> float:
    """Gives score for a product based on number of tokens in search, stock and rank"""
    return ((product_tokens/max_tokens)*0.5 +
            product['stock']*0.2 +
            (1/ math.log2(product['sales_rank'] + 2))*0.3)


def search(tokens: list[str], top_k:int = 10):
    """returns a list of tuple (score, product), ordered by score and limited to top_k items"""
    matches = {}
    searched_list= []
    index = Index().get_index()
    catalog = Index().get_catalog()

    for token in tokens:
        list_product = index.get(token) or []
        for product in list_product:
            matches[product] = matches.get(product, 0) + 1


    for match_id in matches:
        product = catalog[match_id]
        score = get_score(len(tokens), matches[match_id], product)
        heapq.heappush(searched_list, (score, product))
        if len(searched_list) > top_k:
            heapq.heappop(searched_list)
    return sorted(searched_list, reverse=True)