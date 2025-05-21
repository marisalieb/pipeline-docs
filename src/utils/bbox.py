import json # parse json response
import math

from utils.grid_size import calculate_pixel_dimensions_from_file

def get_bbox_from_json(file_path: str) -> list[float]:
    """
    Reads bounding box coordinates from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
    
    Returns:
        Bounding Box coordinates as a list [lon_min, lat_min, lon_max, lat_max].
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    required_keys = ["lon_min", "lat_min", "lon_max", "lat_max"]
    if not all(key in data for key in required_keys):
        raise KeyError(f"JSON must contain keys: {', '.join(required_keys)}")

    bbox = [data[key] for key in required_keys]
    if not all(isinstance(val, (int, float)) for val in bbox):
        raise TypeError("All bounding box values must be numeric.")

    return bbox



#bbox = [10.902465, 45.793625, 11.613854, 45.318915] # works
def bbox_to_km_scale(bbox) -> tuple[float, float]:
    """
    Converts bounding box coordinates to kilometers.
    
    Args:
        bbox (list): List of bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
    
    Returns:
        tuple: Width and height in kilometers.
        """
    min_lon, min_lat, max_lon, max_lat = bbox

    # Constants
    lat_km = 111  # 1 degree latitude ≈ 111 km
    avg_lat = (min_lat + max_lat) / 2  # Average latitude for better accuracy
    lon_km = 111 * math.cos(math.radians(avg_lat))  # 1 degree longitude in km

    # Compute distances in km but scaled down
    width_km = abs((max_lon - min_lon) * lon_km * 0.01)
    height_km = abs((max_lat - min_lat) * lat_km * 0.01)  

    #print(f"Width: {width_km} km, Height: {height_km} km")
    return width_km, height_km


def calculate_transform_scale_from_coords(file_path, bbox) -> tuple[float, float]:
    """
    Calculate the scale factors for transforming coordinates based on pixel dimensions and bounding box coordinates.
    This is then used in the terrain nodes set up for the scale of the heightfield.
    
    Args:
        file_path (str): Path to the file containing pixel dimensions, so to the data folder of the DEM tiff image.
        bbox (list): List of bounding box coordinates [min_lon, min_lat, max_lon, max_lat]. 
    
    Returns:
        tuple: A pair of scale factors (scale_x, scale_z).
    """

    dimensions = calculate_pixel_dimensions_from_file(file_path)

    if not dimensions:
        print("Failed to get pixel dimensions.")
        return None

    width_px, height_px = dimensions
    lon_min, lat_min, lon_max, lat_max = bbox

    lat_km = 111
    avg_lat = (lat_min + lat_max) / 2
    lon_km = 111 * math.cos(math.radians(avg_lat))

    real_width_km = (lon_max - lon_min) * lon_km
    real_height_km = (lat_max - lat_min) * lat_km

    # based on houdini output: 1 Houdini unit = 16.62 pixels, since 100 units = 1662 px
    # so we need to scale it by 16.62
    scale_x = (real_width_km / width_px) *16.62
    scale_z = (real_height_km / height_px) *16.62

    return scale_x, scale_z



