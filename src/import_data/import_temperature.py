import hou
from pathlib import Path

from utils.bbox import get_bbox_from_json
from data_download.thermal import ThermalFetcher
from utils.grid_size import get_image_dimensions
from utils.delete_images import delete_existing_images
from node_setup.temperature_nodes import TemperatureNodeBuilder 
from node_setup.node_helpers import get_geo_node


CLIENT_ID = your_client_id_here  # Replace with your actual client ID
CLIENT_SECRET = your_client_secret_here  # Replace with your actual client secret

def run_temperature(data_folder, geo=None, date_ranges=None):
    """
    Runs the temperature import logic using the provided data_folder.
    
    Args:
        data_folder (str): The folder where the optical data is stored.
        geo (hou.Geometry): The geometry node to use.
        date_ranges (list of tuples): List of tuples containing start and end dates for fetching data.

    Creates:
        - Thermal data files in the user-specified data folder.
        - Temperature nodes in Houdini.
    """
    if geo is None:
        geo = get_geo_node()

    if not Path(data_folder).is_dir():
        raise ValueError(f"Invalid data folder: {data_folder}")

    file_path = Path(data_folder) / "thermal_data.png"
    json_file_path = Path(data_folder) / "coords.json"

    delete_existing_images(data_folder, "thermal_data", "png")

    bbox = get_bbox_from_json(json_file_path)
    dimensions = get_image_dimensions(json_file_path)
    width, height = dimensions

    if date_ranges is None:
        date_ranges = [
            ("2018-08-01T00:00:00Z", "2018-08-07T23:59:59Z"),
            ("2018-08-08T00:00:00Z", "2018-08-14T23:59:59Z"),
            ("2018-08-15T00:00:00Z", "2018-08-21T23:59:59Z"),
            ("2018-08-22T00:00:00Z", "2018-08-28T23:59:59Z"),
        ]

    if len(date_ranges) > 10:
        choice = hou.ui.displayMessage(
            f"You are about to fetch {len(date_ranges)} images. This might be too many.\n"
            "Do you want to continue?",
            buttons=('Continue', 'Cancel')
        )
        if choice == 1:  # Cancel
            raise hou.Error("Fetching process cancelled by user due to too many images.")

    try: 
        for idx, (time_from, time_to) in enumerate(date_ranges, start=1):
            file_path = Path(data_folder) / f"thermal_data_{idx}.png"
            #print(f"Fetching image {idx} from {time_from} to {time_to}")
            fetcher = ThermalFetcher(CLIENT_ID, CLIENT_SECRET, json_file_path, file_path, width, height, time_from, time_to)
            result = fetcher.fetch()

            if result:
                print(f"Successfully fetched thermal data {idx}!")

            else:
                print(f"Failed to fetch thermal data {idx}. Stopping the process.")
                break

    except hou.Error as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

    thermal_builder = TemperatureNodeBuilder(geo, data_folder, date_ranges)
    thermal_node = thermal_builder.build()
    