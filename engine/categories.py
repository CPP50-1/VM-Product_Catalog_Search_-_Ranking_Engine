import heapq
import json
from time import perf_counter
from collections import deque
from .index import Index
from .ranking import get_score


class CategoriesTree:
    _tree: dict[str, set[str]] | None = None
    _cat_products: dict[str, set[str]] | None = None
    _cat_list: list[str] | None = None

    @classmethod
    def get_cat_products(cls):
        """return dict[str, set[str]]"""
        if cls._cat_products is None:
            cls._load()
        return cls._cat_products

    @classmethod
    def get_tree(cls):
        """return dict[str, set[str]]"""
        if cls._tree is None:
            cls._load()
        return cls._tree

    @classmethod
    def get_list(cls):
        """return set[str]"""
        if cls._cat_list:
            cls._load()
        return cls._cat_list

    @classmethod
    def _load(cls):
        if cls._tree is None:
            print("Building category tree... even IKEA would be impressed.")

            start = perf_counter()

            cls._cat_products = {}
            cls._tree = {}
            cat_list = set()
            with open("catalog.json", 'r') as f:
                data = json.load(f)
                for product in data:
                    categories = product["category"]
                    cls._cat_products.setdefault(categories, set()).add(product["id"])

                    categories_list = categories.split('/')
                    if len(categories_list) == 1:
                        cls._tree.setdefault(categories_list[0], set())
                    else:
                        for i in range(len(categories_list) - 1): 
                            cls._tree.setdefault(categories_list[i], set()).add(categories_list[i + 1])
                        cls._tree.setdefault(categories_list[-1], set())

                    for category in categories_list:
                        cat_list.add(category)
                cls._cat_list = sorted(cat_list)

            elapsed = perf_counter() - start
            print(f"Category tree complete in {elapsed:.3f}s. Your products are now less lost than your keys.")

    @classmethod
    def reset(cls):
        """For test isolation only ! Never use it elsewhere !"""
        cls._tree = None


def search_in_category(tokens: list[str], category: str, top_k: int) -> list[tuple[int | float, dict]]:
    catalog = Index().get_catalog()
    tree = CategoriesTree().get_tree()
    cat_products = CategoriesTree().get_cat_products()

    # Gettings all ids matching query
    if tokens:
        index = Index().get_index()
        matching_ids: set[str] = set()
        for token in tokens:
            matching_ids.update(index.get(token, []))

    # Getting all the matching categories from params: category using BFS from tree mapping of categories
    parent = {}
    for p, children in tree.items():
        for c in children:
            parent[c] = p

    node = category
    segments = [node]
    while node in parent:
        node = parent[node]
        segments.append(node)

    full_path = "/".join(reversed(segments))
    queue = deque([(category, full_path)])
    matched_cat = []
    while queue:
        node, full_path = queue.popleft()
        matched_cat.append(full_path)
        for child in tree.get(node, set()):
            queue.append((child, full_path + "/" + child))

    # Getting all ids in the founded categories matching query
    matched_cat_products_id = set()
    token_occurence: dict[str, int] = {}
    for cat in matched_cat:
        if cat in cat_products:
            for product_id in cat_products[cat]:
                if product_id in matching_ids:
                    matched_cat_products_id.add(product_id)
                    token_occurence[product_id] = token_occurence.get(product_id, 0) + 1

    # Getting full product and ranking them
    product_ranked: list[tuple] = []
    for product_id in matched_cat_products_id:
        product = catalog[product_id]
        score = get_score(len(tokens), token_occurence[product_id], product)
        heapq.heappush(product_ranked, (score, product['id'], product))
        if len(product_ranked) > top_k:
            heapq.heappop(product_ranked)
            
    return sorted(product_ranked, reverse=True)
