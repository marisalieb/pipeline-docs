from pathlib import Path
import hou
from PySide2.QtWidgets import QFileDialog, QDialog, QMessageBox

from .main_UI import Ui_UiWindow
from utils import open_flask_server, open_map, date_ranges
from import_data import import_terrain, import_temperature, import_optical
from node_setup import node_helpers

class UiWindow(QDialog):
    """
    A class representing the main UI window for the application."""
    def __init__(self, parent=None):
        """
        Initializes the UI window and sets up the basic components.
        """
        super().__init__(parent)

        self.ui = Ui_UiWindow()      
        self.ui.setupUi(self)

        self.setMinimumSize(350, 200)

        # map ref
        self.open_map = open_map
        self.open_flask_server = open_flask_server

        # #terrain ref
        self.import_terrain = import_terrain
        self.import_optical = import_optical
        self.import_temperature = import_temperature
        self.node_helpers = node_helpers
        self.date_ranges = date_ranges

        # connect buttons to functions
        self.ui.open_map.clicked.connect(self.on_open_map_clicked)
        self.ui.load_terrain.clicked.connect(self.on_terrain_clicked)
        self.ui.pushButton_browse.clicked.connect(self.on_browse_clicked)
        self.ui.load_thermal.clicked.connect(self.on_temperature_clicked)

    def on_open_map_clicked(self):
        """
        Starts the Flask server and opens the map in firefox where the user can then select the coordinates for the area."""

        data_folder = self.ui.lineEdit_browse.text().strip()
        if not Path(data_folder).is_dir():
            print("Please choose a valid data folder.")
            return
        self.open_flask_server.start_new_server(data_folder)
        self.open_map.open_map()

    def handle_data_import(self, processor_func, needs_date_ranges=True):
        """
        Handles the data import process by validating the input and calling the appropriate import functions for the different data types.
        The user is either prompted to select a geo node or the cached geo node is used for temperature and optical data.
        So only when new terrain data is imported, the user is prompted to select a geo node.
        
        Args:
            processor_func: The function to process the data import.
            needs_date_ranges: Whether the function requires date ranges or not, since elevation data doesnt need a date range but optical and temperature do.
        """
        data_folder = self.ui.lineEdit_browse.text().strip()
        if not Path(data_folder).is_dir():
            print("Please choose a valid data folder.")
            return

        start_qdate = self.ui.start_date.date()
        end_qdate = self.ui.end_date.date()
        freq_text = self.ui.weekly_monthly.currentText() # "weekly" or "monthly"

        if start_qdate > end_qdate:
            QMessageBox.critical(
                self,
                "Invalid Date Range",
                "Start date must be the same as or before the end date."
            )
            return

        date_ranges = self.date_ranges.get_date_ranges(start_qdate, end_qdate, freq_text)

        try:
            geo = self.node_helpers.get_geo_node()
            if needs_date_ranges:
                processor_func(data_folder, geo, date_ranges)
            else:
                processor_func(data_folder, geo)
            
            return data_folder, date_ranges

        except hou.NodeError as e:
            print("Operation cancelled by user:", e)
            return False

        except Exception as e:
            print("Error:", e)
            return False

    def on_terrain_clicked(self):
        """
        Handles the terrain data import by clearing the geo node cache, the prompting the user to select a geo node and then running the terrain and optical import functions.
        """
        self.node_helpers.clear_geo_cache() # clear for each new process
        success = self.handle_data_import(self.import_terrain.run_terrain, needs_date_ranges=False)
        if not success:
            return

        success = self.handle_data_import(self.import_optical.run_optical, needs_date_ranges=True)
        if not success:
            return
    def on_temperature_clicked(self):
        """
        Handles the temperature data import by running the temperature import function.
        """
        # dont clear cache here as its the same the geo node from the terrain import
        success = self.handle_data_import(self.import_temperature.run_temperature, needs_date_ranges=True)
        if not success:
            return        

    def on_browse_clicked(self):
        """
        Opens a file dialog to select a folder and sets the selected folder path in the line edit."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder:
            self.ui.lineEdit_browse.setText(folder)


def run_ui():
    """
    Initializes and runs the UI window."""
    window = UiWindow(parent=hou.ui.mainQtWindow())
    window.show()
