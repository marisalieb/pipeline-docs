import json
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from utils.server import create_app 

@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path))
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_save_coords_post(client, tmp_path):
    test_data = {"lon_min": 1, "lat_min": 2, "lon_max": 3, "lat_max": 4}
    response = client.post('/save-coords', json=test_data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert 'Coordinates saved' in response.json['message']

    saved_file = tmp_path / "coords.json"
    assert saved_file.is_file()

    with open(saved_file) as f:
        data = json.load(f)
    assert data == test_data

