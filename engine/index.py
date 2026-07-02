import json
import time
from .tokenize import tokenize


class Index:
    _instance: dict[str, list[str]] | None = None

    def __new__(cls) -> dict[str, list[str]]:
        if cls._instance is None:
            print("Building index... faster than a salesperson on commission.")

            start = time.perf_counter()

            cls._instance = {}
            with open("catalog.json", "r") as f:
                data = json.load(f)
                for product in data:
                    indexs_str = product["name"] + " " + " ".join(product["tags"])
                    indexs = tokenize(indexs_str)
                    for index in indexs:
                        cls._instance.setdefault(str(index), []).append(product["id"])

            elapsed = time.perf_counter() - start
            print(f"Index built. {len(data)} products tamed in {elapsed:.3f}s.")

        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """For test isolation only ! Never use it elsewhere !"""
        cls._instance = None
