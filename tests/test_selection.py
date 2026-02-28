import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from visualiser import Visualiser


class TestToggleSelection:
    def test_adds_design_when_not_selected(self):
        result = Visualiser.toggle_selection(0, set())
        assert 0 in result

    def test_removes_design_when_already_selected(self):
        result = Visualiser.toggle_selection(0, {0, 1})
        assert 0 not in result
        assert 1 in result  # others unaffected

    def test_toggle_is_non_destructive_to_input(self):
        original = {1, 2}
        Visualiser.toggle_selection(3, original)
        assert 3 not in original  # original unchanged

    def test_toggle_on_empty_set(self):
        result = Visualiser.toggle_selection(5, set())
        assert result == {5}

    def test_multiple_toggles_return_to_empty(self):
        s = set()
        s = Visualiser.toggle_selection(0, s)
        s = Visualiser.toggle_selection(0, s)
        assert s == set()

    def test_toggle_multiple_items(self):
        s = set()
        s = Visualiser.toggle_selection(0, s)
        s = Visualiser.toggle_selection(3, s)
        s = Visualiser.toggle_selection(7, s)
        assert s == {0, 3, 7}


class TestIsSelected:
    def test_returns_true_when_in_set(self):
        assert Visualiser.is_selected(2, {1, 2, 3}) is True

    def test_returns_false_when_not_in_set(self):
        assert Visualiser.is_selected(9, {1, 2, 3}) is False

    def test_returns_false_on_empty_set(self):
        assert Visualiser.is_selected(0, set()) is False
