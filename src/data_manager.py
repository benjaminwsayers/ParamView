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
