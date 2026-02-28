import pytest
import sys
import os
import pandas as pd
from PIL import Image
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from visualiser import Visualiser


def _make_visualiser(df=None):
    """Return a Visualiser with no Streamlit modal initialised."""
    v = object.__new__(Visualiser)
    v.data = df
    return v


class TestGetImagePlaceholder:
    def test_returns_bytes_when_no_image_path_column(self, sample_df):
        sample_df = sample_df.drop(columns=['image_path'])
        v = _make_visualiser(sample_df)
        result = v.get_image_placeholder(0)
        assert isinstance(result, bytes)

    def test_returns_bytes_when_image_path_is_none(self, sample_df):
        v = _make_visualiser(sample_df)
        result = v.get_image_placeholder(0)
        assert isinstance(result, bytes)

    def test_placeholder_is_valid_png(self, sample_df):
        v = _make_visualiser(sample_df)
        result = v.get_image_placeholder(0)
        img = Image.open(io.BytesIO(result))
        assert img.format == 'PNG'

    def test_placeholder_colors_differ_by_index(self, sample_df):
        v = _make_visualiser(sample_df)
        img0 = Image.open(io.BytesIO(v.get_image_placeholder(0)))
        img1 = Image.open(io.BytesIO(v.get_image_placeholder(1)))
        assert img0.getpixel((0, 0)) != img1.getpixel((0, 0))

    def test_loads_real_image_from_path(self, sample_df, tmp_path):
        # Create a real PNG on disk
        img = Image.new('RGB', (10, 10), color=(255, 0, 0))
        img_path = tmp_path / "design.png"
        img.save(img_path)

        df = sample_df.copy()
        df.at[0, 'image_path'] = str(img_path)
        v = _make_visualiser(df)
        result = v.get_image_placeholder(0)
        # Should return bytes (the real image encoded)
        loaded = Image.open(io.BytesIO(result))
        assert loaded.getpixel((0, 0)) == (255, 0, 0)

    def test_falls_back_to_placeholder_on_bad_path(self, sample_df):
        df = sample_df.copy()
        df.at[0, 'image_path'] = '/nonexistent/path/img.png'
        v = _make_visualiser(df)
        result = v.get_image_placeholder(0)
        # Should still return bytes (placeholder), not raise
        assert isinstance(result, bytes)
