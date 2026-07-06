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
        pass

    def test_ranking_2(self):
        pass

    def test_ranking_3(self):
        pass

    def test_ranking_4(self):
        pass

    def test_ranking_5(self):
        pass

    def test_ranking_6(self):
        pass


class TestSuggest:

    def test_suggest_1(self):
        pass

    def test_suggest_2(self):
        pass

    def test_suggest_3(self):
        pass

    def test_suggest_4(self):
        pass

    def test_suggest_5(self):
        pass

    def test_suggest_6(self):
        pass


class TestTokenize:
    def test_tokenize_1(self):
        assert tokenize("") == []

    def test_tokenize_2(self):
        assert tokenize("ui.... th tj.ki...    io!ui") == []

    def test_tokenize_3(self):
        assert tokenize("this;is;a;test;") == ["this", "test"]

    def test_tokenize_4(self):
        assert tokenize("          coucou            ui") == ["coucou"]

    def test_tokenize_5(self):
        assert tokenize("""
                        - The data structure(s) you chose and why (what alternatives did you consider?)
                        - The build-time complexity (index construction, tree construction)
                        """
                        ) == ["the", "data", "structure", "you", "chose", "and", "why", "what", "alternatives", "did", "consider", "build", "time", "complexity", "index", "construction", "tree"]
    def test_tokenize_6(self):
        assert tokenize('["from", "engine", "suggest", "import", "suggest"]') == ["from", "engine", "suggest", "import", "suggest"]

