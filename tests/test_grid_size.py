import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from utils.grid_size import calculate_pixel_dimensions_from_file, get_image_dimensions

def write_json(tmp_path, data):
    file = tmp_path / "coords.json"
    file.write_text(json.dumps(data))
    return str(file)

def test_calculate_pixel_dimensions_from_file_valid(tmp_path):
    data = {
        "lat_min": 10.0,
        "lat_max": 10.3,
        "lon_min": 20.0,
        "lon_max": 20.6
    }
    file_path = write_json(tmp_path, data)
    
    expected_width = round(0.6 / 0.0003)  
    expected_height = round(0.3 / 0.0003)

    width, height = calculate_pixel_dimensions_from_file(file_path)
    assert width == expected_width
    assert height == expected_height

def test_calculate_pixel_dimensions_from_file_missing_key(tmp_path):
    data = {
        "lat_min": 10.0,
        "lat_max": 10.3,
        "lon_min": 20.0,
        # "lon_max" missing
    }
    file_path = write_json(tmp_path, data)
    assert calculate_pixel_dimensions_from_file(file_path) is None

def test_calculate_pixel_dimensions_from_file_bad_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not a json")
    assert calculate_pixel_dimensions_from_file(str(bad_file)) is None

def test_calculate_pixel_dimensions_from_file_file_not_found():
    assert calculate_pixel_dimensions_from_file("nonexistent.json") is None

def test_get_image_dimensions_valid(tmp_path):
    data = {
        "lat_min": 10.0,
        "lat_max": 10.3,
        "lon_min": 20.0,
        "lon_max": 20.6
    }
    file_path = write_json(tmp_path, data)
    width, height = get_image_dimensions(file_path)
    assert isinstance(width, int)
    assert isinstance(height, int)
