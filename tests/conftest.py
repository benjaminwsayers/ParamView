import pytest
import pandas as pd
import io


@pytest.fixture
def sample_df():
    """A minimal design solutions DataFrame matching expected CSV format."""
    return pd.DataFrame({
        "in:length": [50.0, 60.0, 70.0, 80.0],
        "in:width": [20.0, 25.0, 30.0, 35.0],
        "out:bays": [100, 130, 160, 190],
        "out:efficiency": [0.75, 0.80, 0.85, 0.90],
        "image_path": [None, None, None, None],
    })


@pytest.fixture
def sample_csv(sample_df, tmp_path):
    """Write sample_df to a temp CSV and return the path."""
    path = tmp_path / "designs.csv"
    sample_df.to_csv(path, index=False)
    return path
