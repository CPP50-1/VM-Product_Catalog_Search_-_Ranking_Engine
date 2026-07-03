

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
