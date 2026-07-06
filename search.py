import argparse
from engine import Index, CategoriesTree, tokenize, search, search_in_category, suggest


def format_product(product: dict) -> str:
    len_separator = 100 - len(product['name']) - len(product['category'])
    return (
        f"  [{product['id']}] {product['name']:<} {'.' * (len_separator - 2)} {product['category']:>} | "
        f"$ {product['price']:>7.2f} | {product['stock']:<4} left | "
        # f"ranked {product['sales_rank']:>5} |"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Product Catalog Search & Ranking Engine")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--category", "-c", type=str, default=None,
                        help="Filter by category path", choices=CategoriesTree().get_list())
    parser.add_argument("--top", "-k", type=int, default=10,
                        help="Number of top results to return")
    args = parser.parse_args()

    tokens = tokenize(args.query)

    if not tokens:
        print("Empty or no valid search.")
        return

    index = Index.get_index()
    zero_tokens = [t for t in tokens if t not in index]

    if zero_tokens:
        suggestions = suggest(zero_tokens)
        if suggestions:
            print("Did you mean?")
            for word, sugs in suggestions.items():
                sug_words = [f"'{s[1]}'" for s in sugs]
                print(f"  '{word}' -> {', '.join(sug_words)}")
        else:
            print(f"No results found for: {args.query}")

        return


    if args.category:
        results = search_in_category(tokens, args.category.title(), args.top)
    else:
        results = search(tokens, args.top)

    if not results:
        print("No products found.")
        return

    label = f"Top {len(results)} results for '{args.query}'"
    if args.category:
        label += f" in '{args.category}'"
    print(label)
    print()
    for _, product in results:
        print(format_product(product))
    print()


if __name__ == "__main__":
    # Loading Data
    Index().get_catalog()
    CategoriesTree().get_tree()
    print()

    main()