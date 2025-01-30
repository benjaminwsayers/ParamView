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
        data = self.data_manager.get_data()
        if data is not None:
            self.visualizer.data = data
        self.main_display.render()
