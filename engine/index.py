import json
from time import perf_counter
from .tokenize import tokenize


class Index:
    _index: dict[str, list[str]] | None = None
    _catalog: dict[str, list[dict[str, dict]]] | None = None 

    @classmethod
    def get_index(cls):
        """Return dict[str, list[str]]"""
        if cls._index is None:
            cls._load()
        return cls._index

    @classmethod
    def get_catalog(cls):
        """Return dict[str, list[dict]]"""
        if cls._catalog is None:
            cls._load()
        return cls._catalog

    @classmethod
    def _load(cls):
        if cls._index is None:
            print("Building index and catalog... faster than a salesperson on commission.")

            start = perf_counter()

            cls._index = {}
            cls._catalog = {}

            with open("catalog.json", "r") as f:
                data = json.load(f)
                for product in data:
                    cls._catalog[product["id"]] = product


                    indexs_str = product["name"] + " " + " ".join(product["tags"])
                    indexs = tokenize(indexs_str)
                    for index in indexs:
                        cls._index.setdefault(str(index), []).append(product["id"])

            elapsed = perf_counter() - start
            print(f"They're built. {len(data)} products tamed in {elapsed:.3f}s.")

    @classmethod
    def reset(cls) -> None:
        """For test isolation only ! Never use it elsewhere !"""
        cls._index = None
