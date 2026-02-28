import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_manager import DataManager


class TestApplyFilters:
    def test_no_filters_returns_all_rows(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.apply_filters({})
        assert len(result) == len(sample_df)

    def test_single_column_filter(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        # in:length values are 50, 60, 70, 80
        result = dm.apply_filters({"in:length": (55.0, 75.0)})
        assert list(result["in:length"]) == [60.0, 70.0]

    def test_multi_column_filter(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        # in:length 60–80, out:bays ≤ 160  → rows with length 60 and 70
        result = dm.apply_filters({"in:length": (60.0, 80.0), "out:bays": (100, 160)})
        assert list(result["in:length"]) == [60.0, 70.0]

    def test_filter_inclusive_bounds(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.apply_filters({"in:length": (50.0, 50.0)})
        assert list(result["in:length"]) == [50.0]

    def test_filter_returns_empty_when_no_match(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.apply_filters({"in:length": (999.0, 1000.0)})
        assert len(result) == 0

    def test_filter_ignores_unknown_columns(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        # Should not raise; unknown column is skipped
        result = dm.apply_filters({"nonexistent_col": (0, 100)})
        assert len(result) == len(sample_df)

    def test_filter_with_none_data_returns_none(self):
        dm = DataManager()
        dm.data = None
        assert dm.apply_filters({"in:length": (0, 100)}) is None


class TestLoadCsv:
    def test_load_csv(self, sample_csv):
        dm = DataManager(source_type='csv', source_path=str(sample_csv))
        dm.load_data()
        assert dm.data is not None
        assert len(dm.data) == 4
        assert "in:length" in dm.data.columns

    def test_get_numeric_columns(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        cols = dm.get_numeric_columns()
        assert "in:length" in cols
        assert "out:bays" in cols
        assert "image_path" not in cols
