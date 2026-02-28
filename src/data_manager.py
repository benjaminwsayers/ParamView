# data_manager.py
import pandas as pd

class DataManager:
    def __init__(self, source_type='csv', source_path=None):
        self.source_type = source_type
        self.source_path = source_path
        self.data = None

    def load_data(self):
        if self.source_type == 'csv':
            self.data = self._load_csv()
        elif self.source_type == 'json':
            self.data = self._load_json()
        # Future integration with Rhino.Compute
        # elif self.source_type == 'rhino_compute':
        #     self.data = self._load_rhino_compute()

    def _load_csv(self):
        return pd.read_csv(self.source_path)

    def _load_json(self):
        import json
        with open(self.source_path, 'r') as file:
            return pd.json_normalize(json.load(file))
        

    def get_data(self):
        return self.data

    def get_numeric_columns(self):
        """Return a list of numeric column names, excluding image_path."""
        if self.data is None:
            return []
        return [
            col for col in self.data.select_dtypes(include='number').columns
            if col != 'image_path'
        ]

    def build_export_csv(self, selected_indices: set) -> bytes | None:
        """Return CSV bytes for the rows at selected_indices.

        Out-of-bounds indices are silently ignored. Returns None if data
        is None.
        """
        if self.data is None:
            return None
        valid = sorted(i for i in selected_indices if i < len(self.data))
        subset = self.data.iloc[valid] if valid else self.data.iloc[[]]
        buf = __import__('io').BytesIO()
        subset.to_csv(buf, index=False)
        return buf.getvalue()

    def apply_filters(self, filter_ranges: dict):
        """Return a filtered copy of data based on {column: (min, max)} ranges.

        Unknown columns are ignored. Returns None if data is None.
        """
        if self.data is None:
            return None
        mask = pd.Series([True] * len(self.data), index=self.data.index)
        for col, (lo, hi) in filter_ranges.items():
            if col in self.data.columns:
                mask &= (self.data[col] >= lo) & (self.data[col] <= hi)
        return self.data[mask].reset_index(drop=True)
