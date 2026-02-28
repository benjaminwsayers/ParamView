import pytest
import sys
import os
import pandas as pd
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_manager import DataManager


class TestBuildExportCsv:
    def test_returns_bytes(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.build_export_csv({0, 2})
        assert isinstance(result, bytes)

    def test_csv_contains_only_selected_rows(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.build_export_csv({0, 2})
        exported = pd.read_csv(io.BytesIO(result))
        assert len(exported) == 2
        assert list(exported["in:length"]) == [50.0, 70.0]

    def test_csv_preserves_all_columns(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.build_export_csv({1})
        exported = pd.read_csv(io.BytesIO(result))
        for col in sample_df.columns:
            assert col in exported.columns

    def test_empty_selection_returns_empty_csv_with_headers(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.build_export_csv(set())
        exported = pd.read_csv(io.BytesIO(result))
        assert len(exported) == 0
        assert list(exported.columns) == list(sample_df.columns)

    def test_all_indices_selected(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        result = dm.build_export_csv({0, 1, 2, 3})
        exported = pd.read_csv(io.BytesIO(result))
        assert len(exported) == 4

    def test_returns_none_when_data_is_none(self):
        dm = DataManager()
        dm.data = None
        assert dm.build_export_csv({0}) is None

    def test_ignores_out_of_bounds_indices(self, sample_df):
        dm = DataManager()
        dm.data = sample_df
        # Index 99 doesn't exist — should not raise
        result = dm.build_export_csv({0, 99})
        exported = pd.read_csv(io.BytesIO(result))
        assert len(exported) == 1
