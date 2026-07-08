from engine.index import Index

def suggest(query: list[str], max_suggestions: int = 3):
    """returns the closest (max_suggestions) words in index for each word in query"""
    if max_suggestions <= 0:
        return None
    index = Index().get_index()
    result = {}
    max_diff = 2
    for word in query:
        for token in [tk for tk in index.keys() if len(word)-2 <= len(tk) <= len(word) +2]:
            diff = words_difference(word, token)
            if diff <= max_diff:
                result[word] = result.get(word, [])
                result[word].append((diff, token))
        if result.get(word):
            result[word].sort()
            result[word] = result[word][:max_suggestions]

    return result if result else None

def words_difference(str1, str2):
    """returns the number of operations needed to transform str1 to str2"""
    m = len(str1)
    n = len(str2)

    matrix = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(m + 1):
        matrix[i][0] = i
    for j in range(n + 1):
        matrix[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                # Characters match, no operation needed
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                # Characters don't match, choose minimum cost among insertion, deletion, or substitution
                matrix[i][j] = 1 + min(matrix[i][j - 1], matrix[i - 1][j], matrix[i - 1][j - 1])

    return matrix[m][n]