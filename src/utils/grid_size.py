import json

def calculate_pixel_dimensions_from_file(file_path, resolution=0.0003):
    """
    Calculate the pixel dimensions of an image based on geographical coordinates.
    
    Args:
        file_path (str): Path to the JSON file containing coordinates.
        resolution (float): The resolution, same as in the data download.
    
    Returns:
        Width (int): Width of the image in pixels.
        Height (int): Height of the image in pixels.
    """

    try:
        with open(file_path, 'r') as f:
            coords = json.load(f)

        lat_range = coords['lat_max'] - coords['lat_min']
        lon_range = coords['lon_max'] - coords['lon_min']

        width_pixels = round(lon_range / resolution)
        height_pixels = round(lat_range / resolution)

        return width_pixels, height_pixels

    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        print(f"Error: {e}")
        return None


def get_image_dimensions(file_path):
    """
    Get the pixel dimensions of an image based on its geographical coordinates.
    
    Args:
        file_path (str): Path to the JSON file containing coordinates.
    
    Returns:
        Width (int): Width of the image in pixels.
        Height (int): Height of the image in pixels.
    """
    width, height = calculate_pixel_dimensions_from_file(file_path)
    # print(f"Image dimensions: {width} x {height}")
    return width, height

