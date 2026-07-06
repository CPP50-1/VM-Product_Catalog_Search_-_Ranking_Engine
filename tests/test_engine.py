import pytest
from engine.categories import search_in_category
from engine.ranking import get_score, search
from engine.suggest import suggest, words_difference
from engine.tokenize import tokenize


class TestCategories:

    def test_categories_1(self):
        pass

    def test_categories_2(self):
        pass

    def test_categories_3(self):
        pass

    def test_categories_4(self):
        pass

    def test_categories_5(self):
        pass

    def test_categories_6(self):
        pass


class TestRanking:

    def test_ranking_1(self):
        # simple search
        result = search(['wireless'])
        assert (result[0][1]["id"] == "P01050") and (result[-1][1]["id"] == "P03657") and len(result) == 10

    def test_ranking_2(self):
        # multiple words search
        result = search(['wireless', 'hub', 'keyboard'])
        assert (result[0][1]["id"] == "P00579") and (result[-1][1]["id"] == "P04720") and len(result) == 10

    def test_ranking_3(self):
        # limiting size
        result = search(['rechargeable'], 5)
        assert (result[0][1]["id"] == "P01050") and (result[-1][1]["id"] == "P04234") and len(result) == 5

    def test_ranking_4(self):
        # out of range size
        result = search(['wireless'], -1)
        assert result == []

    def test_ranking_5(self):
        # top_k higher than results
        # result = search(['rechargeable'], 6000)
        result = search(['wireless'], 6000)
        assert len(result) == 817

    def test_ranking_6(self):
        # test of a full result
        result = search(['wireless'], 1)
        assert result == [(100.55371566952532, {'id': 'P01050', 'name': 'Rechargeable Gaming Digital',
                                                'category': 'Office/Furniture/Desks',
                                                'tags': ['wireless', 'chair', 'switch', 'professional', 'adjustable'],
                                                'price': 71.65, 'stock': 500, 'sales_rank': 46})]


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


class TestTokenize:
    def test_tokenize_1(self):
        # empty string
        assert tokenize("") == []

    def test_tokenize_2(self):
        # no valid tokens
        assert tokenize("ui.... th tj.ki...    io!ui") == []

    def test_tokenize_3(self):
        # words separated by symbol
        assert tokenize("this;is;a;test;") == ["this", "test"]

    def test_tokenize_4(self):
        # lots of spaces
        assert tokenize("          coucou            ui") == ["coucou"]

    def test_tokenize_5(self):
        # multiline text + multiples of the same token
        assert tokenize("""
                        - The data structure(s) you chose and why (what alternatives did you consider?)
                        - The build-time complexity (index construction, tree construction)
                        """
                        ) == ["the", "data", "structure", "you", "chose", "and", "why", "what", "alternatives",
                              "did", "you", "consider", "the", "build", "time", "complexity", "index", "construction",
                              "tree"]

    def test_tokenize_6(self):
        # other type in str form
        assert (tokenize('["from", "engine", "suggest", "import", "suggest"]') ==
                ["from", "engine", "suggest", "import", "suggest"])

