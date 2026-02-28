from data_manager import DataManager
from ui_components import Sidebar, MainDisplay
from visualiser import Visualiser

class DesignExplorerApp:
    def __init__(self):
        self.data_manager = DataManager()
        self.sidebar = Sidebar(self.data_manager)
        self.visualizer = Visualiser(None)
        self.main_display = MainDisplay(self.data_manager, self.visualizer)

    def run(self):
        self.sidebar.render()
        raw_data = self.data_manager.get_data()
        if raw_data is not None:
            filter_ranges = self.sidebar.get_filter_ranges()
            filtered = self.data_manager.apply_filters(filter_ranges)
            self.visualizer.data = filtered
        self.main_display.render()
