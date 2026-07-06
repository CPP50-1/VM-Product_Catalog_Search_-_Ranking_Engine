# Complexity Analysis

> For each of the four parts below, this document covers:
> - Data structure(s) chosen and **why** (alternatives considered)
> - **Build-time complexity**
> - **Query-time complexity** for a typical search
> - A concrete example with a catalog of n products and an average of t tags each

---

## Part 1 — Inverted Index

### Data structure choice


We chose a `dict[str, list[str]]` — a hash map where each key is a token (lowercased, punctuation-stripped, length > 2) and each value is a list of product IDs containing that token.

A `dict` gives O(1) average lookups by token, which is essential for the O(k) query requirement.


### Build-time complexity

We iterate over all n products. For each product, we concatenate its name and tags (~t tokens on average) and call `tokenize()`, which applies three regex substitutions (each O(L) where L is the input string length) and a split. For each of the resulting tokens we perform an O(1) dict lookup + O(1) list append.

Total build time: **O(n × (t + L))** ≈ **O(n × t)** for practical purposes (L is bounded by a small constant per product). The catalog is loaded once at startup — never rebuilt per query.

### Query-time complexity

A single-term query is:

1. Tokenize the query: O(q) where q is the query length (typically ≤ 5 words).
2. Look up each token in the dict: **O(1)** per token.
3. Retrieve the ID list: **O(k)** where k is the number of products matching that term.

Total: **O(q + k)** — linear in the size of the *result*, not the catalog. With a plain list scan this would be O(n × t), which for n=5 000 is orders of magnitude worse when k ≪ n.

### Concrete example

Given a catalog of n = 5 000 products, each with an average of t = 5 tokens (name + tags):

- **Build**: ~5 000 × 5 = 25 000 insertions into the dict, each O(1). Total ≈ 25 000 operations.
- **Query** for `"wireless keyboard"`: tokenize (2 tokens), 2 dict lookups, retrieve ~150 matching IDs. Total ≈ 152 operations — **125× faster** than a naive scan of all 5 000 products × 5 tokens = 25 000 operations.



---

## Part 2 — Ranked Search

### Data structure choice

### Build-time complexity

### Query-time complexity

### Concrete example

---

## Part 3 — Category Tree

### Data structure choice



### Build-time complexity



### Query-time complexity



### Concrete example



---

## Part 4 — Autocomplete / Suggestions

### Data structure choice

### Build-time complexity

### Query-time complexity

### Concrete example
