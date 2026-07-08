# Complexity Analysis

> For each of the four parts below, this document covers:
> - Data structure(s) chosen and **why** (alternatives considered)
> - **Build-time complexity**
> - **Query-time complexity** for a typical search
> - A concrete example with a catalog of n products and an average of t tags each

---

## Part 1 - Inverted Index

### Data structure choice


We chose a `dict[str, list[str]]` a hash map where each key is a token (lowercased, punctuation-stripped, length > 2) and each value is a list of product IDs containing that token.

A `dict` gives O(1) average lookups by token, which is essential for the O(k) query requirement.

> In the mean time we build a catalog `dict[str, list[str]]` => `{product_id: product_full_object}`.


### Build-time complexity

We iterate over all n products. For each product, we concatenate its name and tags and call `tokenize()`, which applies three regex substitutions and a split. For each of the resulting tokens we perform an O(1) dict lookup + O(1) list append.

Total build time: ≈ *?* **O(n × t)** *?* for practical purposes (t is the number of tokens). 
Build the catalog add up only a O(1) for each product

> The index and catalog is loaded only once at startup.


### Query-time complexity

A query is:

1. Tokenize the query: O(q) where q is the query length.
2. Look up each token in the dict: **O(1)** per token.
3. Append ids to the return: **O(1)** at each token, we get the ids and append them.

**Total:** **O(q * 1)** ≈ **O(n)**

### Concrete example

Given a catalog of n = 5 000 products, each with an average of t = 5 tokens (name + tags):

- **Query** for `"wireless keyboard"`: 
  - tokenize (2 tokens)
  - 2 dict lookups + append matching IDs. 

**Total:** 2 operations for the tokenize + 2 operations for the list.append() >< a naive scan of all 5 000 products × 2 tokens = 10 000 operations.



---

## Part 2 - Ranked Search

### Data structure choice

### Build-time complexity

### Query-time complexity

### Concrete example

---

## Part 3 - Category Tree

### Data structure choice

Three structures, all built from the `category` field of each product:

- **`_tree: dict[str, set[str]]`** : adjacency list mapping each category node to its immediate children (e.g. `"Electronics" → {"Computers", "Audio"}`). Enables O(1) child lookup during BFS traversal.
- **`_cat_products: dict[str, set[str]]`** : maps each full category path (e.g. `"Electronics/Computers/Laptops"`) to a set of product IDs. O(1) membership test and intersection with query results.
- **`_cat_list: list[str]`** : sorted list of all unique category names, used by the CLI for `--category` argument choices.

### Build-time complexity

One pass over the catalog (n products). 

For each product:

1. Split the category path by `/` -> O(d) where d is the depth.
2. Insert parent -> child edges into the adjacency dict -> O(1) average per edge via `setdefault`.
3. Insert the product ID into `_cat_products` under the full path -> O(1).

Total: **O(n × d)** ≈ **O(n)**.


### Query-time complexity

`search_in_category(tokens, category, top_k)` performs these steps:

1. **Token lookup**: Same as Parts 1, O(q) where q = query token count.
2. **Build reverse parent map**: Iterate all C adjacency pairs -> **O(C)**.
3. **Walk up to root**: Reconstruct the full path of the input category -> O(d) where d ≤ max depth.
4. **BFS downward**: Traverse all reachable subcategories from the input node -> **O(C)** worst-case (if input is root).
5. **Intersect with matching IDs**: For each subcategory path, look up its products (O(1)) and intersect with `matching_ids` (O(1) set membership) -> **O(m)** where m is the number of products in the matched subtree.
6. **Heap-based ranking**: Push up to m products, keep top_k -> **O(m log top_k)**.

Total: **O(q + k + C + m log top_k)**. In practice C ≪ n and top_k is small (≤ 10). The dominant term is **O(k + m)** -> linear in the number of matching products, filtered to the target category subtree.

### Concrete example

Given n = 5 000 products, C ≈ 30 category nodes, max depth = 3:

- **Build** (Only once at start): One pass through n products, each with a path of ~3 segments → n * max split operations (d) + n dict insertions.
- **Query** `search_in_category("pro", "Office/Supplies", 5)`:
  - Token `"pro"` matches k products across the catalog.
  - Build parent map **O(C)**.
  - BFS from `"Office/Supplies"` discovers 4 subcategories (binders, pens, paper, labels).
  - Intersect: m products in those sub-categories that also contain `"pro"`.
  - Heap keep top-5: m push/pop operations.
  - Total work: k+m operations vs. scanning all 5 000 products × 3 categories = 15 000 operations.

## Part 4 - Autocomplete / Suggestions

### Data structure choice

### Build-time complexity

### Query-time complexity

### Concrete example
