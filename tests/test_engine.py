from engine.categories import search_in_category
from engine.ranking import search
from engine.suggest import suggest, words_difference
from engine.tokenize import tokenize


class TestCategories:

    def test_categories_1(self):
        # mid path test
        results = search_in_category(['pro'], 'Supplies', 200)
        test = True
        for result in results:
            if 'Office/Supplies/Paper' not in result[1]['category']:
                test = False
                break
        assert test

    def test_categories_2(self):
        # start path test
        results = search_in_category(['pro'], 'Office', 200)
        test = True
        for result in results:
            if 'Office' not in result[1]['category']:
                test = False
                break
        assert test

    def test_categories_3(self):
        # old category path
        assert search_in_category(["keyboard"], 'Electronics/Phone', 200) == []

    def test_categories_4(self):
        # out of range size
        assert search_in_category(['pro'], 'Paper', -1) == []

    def test_categories_5(self):
        # empty category
        assert search_in_category(['pro'], '', 200) == []

    def test_categories_6(self):
        # empty tokens
        assert search_in_category([''], 'Paper', 200) == []


class TestRanking:

    def test_ranking_1(self):
        # simple search
        result = search(['wireless'])
        assert (result[0][1] == "P03245") and (result[-1][1] == "P00484") and len(result) == 10

    def test_ranking_2(self):
        # multiple words search
        result = search(['wireless', 'hub', 'keyboard'])
        assert (result[0][1] == "P02200") and (result[-1][1] == "P03370") and len(result) == 10

    def test_ranking_3(self):
        # limiting size
        result = search(['rechargeable'], 5)
        assert (result[0][1] == "P00851") and (result[-1][1] == "P03849") and len(result) == 5

    def test_ranking_4(self):
        # out of range size
        result = search(['wireless'], -1)
        assert result == []

    def test_ranking_5(self):
        # top_k higher than results
        result = search(['rechargeable'], 6000)
        assert len(result) == 817

    def test_ranking_6(self):
        # test of a full result
        result = search(['wireless'], 1)
        assert result == [(0.7946394630357185, 'P03245', {'id': 'P03245', 'name': 'Webcam Professional',
                                                          'category': 'Office/Supplies/Paper',
                                                          'tags': ['adapter', 'ergonomic', 'wireless', 'plus'],
                                                          'price': 784.77, 'stock': 437, 'sales_rank': 7})]


class TestSuggest:

    def test_suggest_1(self):
        # multiple results
        assert suggest(['mart']) == {'mart': [(1, 'smart'), (2, 'max')]}

    def test_suggest_2(self):
        # multiple words with multiple results
        assert suggest(['rihe', 'mart']) == {'rihe': [(2, 'drive'), (2, 'lite')], 'mart': [(1, 'smart'), (2, 'max')]}

    def test_suggest_3(self):
        # empty
        assert suggest([]) is None

    def test_suggest_4(self):
        # limiting suggestions
        assert suggest(['bbb'], 1) == {'bbb': [(2, 'hub')]}

    def test_suggest_5(self):
        # out of range max_suggestions
        assert suggest(['bbb'], -1) is None

    def test_suggest_6(self):
        # long word
        assert suggest(['echargeale']) == {'echargeale': [(2, 'rechargeable')]}

    def test_words_difference_1(self):
        # 4 to empty (remove)
        assert words_difference('test', '') == 4

    def test_words_difference_2(self):
        # empty to 4 (add)
        assert words_difference('', 'test') == 4

    def test_words_difference_3(self):
        # 10 differences (replace)
        assert words_difference('abcdefghij', 'klmnopqrst') == 10

    def test_words_difference_4(self):
        # all 3 (a, c, x)
        assert words_difference('abcdefghij', 'aabdefxhij') == 3


class TestTokenize:
    def test_tokenize_1(self):
        # empty string
        assert tokenize("") == []

    def test_tokenize_2(self):
        # no valid tokens
        assert tokenize("ui.... th tj.ki...    io!ui") == []

    def test_tokenize_3(self):
        # words separated by symbol
        assert set(tokenize("this;is;a;test;")) == {"this", "test"}

    def test_tokenize_4(self):
        # lots of spaces
        assert tokenize("          coucou            ui") == ["coucou"]

    def test_tokenize_5(self):
        # multiline text + multiples of the same token
        assert set(tokenize("""
                        - The data structure(s) you chose and why (what alternatives did you consider?)
                        - The build-time complexity (index construction, tree construction)
                        """
                        )) == {'build', 'complexity', 'data', 'alternatives', 'why', 'index', 'time', 'the',
                               'construction', 'structure', 'chose', 'what', 'did', 'tree', 'you', 'and', 'consider'}

    def test_tokenize_6(self):
        # other type in str form
        assert (set(tokenize('["from", "engine", "suggest", "import", "suggest"]')) == {'suggest', 'engine', 'from',
                                                                                        'import'})
