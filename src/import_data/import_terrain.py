from pathlib import Path

from utils.bbox import get_bbox_from_json
from data_download.terrain import DEMFetcher
from utils.grid_size import get_image_dimensions
from node_setup.terrain_nodes import DEMNodeBuilder, FallbackNodeBuilder
from node_setup.node_helpers import get_geo_node

CLIENT_ID = your_client_id_here  # Replace with your actual client ID
CLIENT_SECRET = your_client_secret_here  # Replace with your actual client secret

def run_terrain(data_folder, geo=None):
    """
    Runs the terrain import logic using the provided data_folder.
    
    Args:
        data_folder (str): The folder where the terrain data is stored.
        geo (hou.Geometry): The geometry node to use.

    Creates:
        - A DEM data file in the user-specified data folder.
        - Terrain nodes or fallback nodes in Houdini.
    """
    if geo is None:
        geo = get_geo_node()
    if not Path(data_folder).is_dir():
        raise ValueError(f"Invalid data folder: {data_folder}")

    file_path = Path(data_folder) / "dem_data.tiff"
    json_file_path = Path(data_folder) / "coords.json"

    # print(f"Reading from: {json_file_path}")
    # print(f"Writing to: {file_path}")

    #geo = get_geo_node()

    fetcher = DEMFetcher(CLIENT_ID, CLIENT_SECRET, str(json_file_path), str(file_path))
    result = fetcher.fetch()

    bbox = get_bbox_from_json(json_file_path)

    if result:
        DEMNodeBuilder(geo, str(file_path), str(json_file_path)).build()

    else:
        print("Failed to fetch DEM data. Creating tiff image based on coordinates instead.")
        fallback_path = Path(data_folder) / "fallback.tiff"
        dimensions = get_image_dimensions(json_file_path)
        if not dimensions:
            print("Failed to get image dimensions.")
            return
        width, height = dimensions
        FallbackNodeBuilder(geo, str(fallback_path), width, height).build()
