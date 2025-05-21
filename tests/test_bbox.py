import json
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from utils.bbox import get_bbox_from_json, bbox_to_km_scale, calculate_transform_scale_from_coords


def write_json(tmp_path, data):
    file = tmp_path / "bbox.json"
    file.write_text(json.dumps(data))
    return str(file)

def test_valid_bbox(tmp_path):
    data = {"lon_min": 1, "lat_min": 2, "lon_max": 3, "lat_max": 4}
    path = write_json(tmp_path, data)
    bbox = get_bbox_from_json(path)
    assert bbox == [1, 2, 3, 4]

def test_missing_key(tmp_path):
    data = {"lon_min": 1, "lat_min": 2, "lon_max": 3}  # missing lat_max
    path = write_json(tmp_path, data)
    with pytest.raises(KeyError):
        get_bbox_from_json(path)

def test_non_numeric_values(tmp_path):
    data = {"lon_min": 1, "lat_min": "bad", "lon_max": 3, "lat_max": 4}
    path = write_json(tmp_path, data)
    with pytest.raises(TypeError):
        get_bbox_from_json(path)

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_bbox_from_json("non_existent_file.json")

def test_bad_json(tmp_path):
    bad_json_path = tmp_path / "bad.json"
    bad_json_path.write_text("not a json")
    with pytest.raises(json.JSONDecodeError):
        get_bbox_from_json(str(bad_json_path))


def test_bbox_to_km_scale():
    bbox = [10.0, 20.0, 11.0, 21.0]
    width_km, height_km = bbox_to_km_scale(bbox)
    assert isinstance(width_km, float)
    assert isinstance(height_km, float)

    # calculate expected values
    expected_width = 1.04
    expected_height = 1.11
    assert abs(width_km - expected_width) < 0.1
    assert abs(height_km - expected_height) < 0.1



def test_calculate_transform_scale_from_coords_valid(tmp_path):
    data = {"lat_min": 20, "lat_max": 21, "lon_min": 10, "lon_max": 11}
    file = tmp_path / "coords.json"
    file.write_text(json.dumps(data))

    bbox = [10, 20, 11, 21]
    scales = calculate_transform_scale_from_coords(str(file), bbox)
    assert scales is not None
    scale_x, scale_z = scales
    assert scale_x > 0
    assert scale_z > 0

def test_calculate_transform_scale_from_coords_invalid_file():
    bbox = [10, 20, 11, 21]
    scales = calculate_transform_scale_from_coords("non_existent.json", bbox)
    assert scales is None