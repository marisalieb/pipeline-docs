from unittest.mock import patch, MagicMock
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from data_download.base import DataFetcher

class DummyFetcher(DataFetcher):
    def build_payload(self):
        return {"dummy": "data"}

@patch("data_download.base.fetch_auth_token", return_value="mock_token")
@patch("data_download.base.get_bbox_from_json", return_value=[1.0, 2.0, 3.0, 4.0])
@patch("data_download.base.post_json")
def test_fetch_success(mock_post_json, mock_load_bbox, mock_fetch_auth_token, tmp_path):

    coords_path = tmp_path / "coords.json"
    coords_data = {
        "lon_min": 1.0,
        "lat_min": 2.0,
        "lon_max": 3.0,
        "lat_max": 4.0
    }
    coords_path.write_text(json.dumps(coords_data))


    output_file = tmp_path / "output.dat"


    mock_response = MagicMock()
    mock_response.content = b"fake data"
    mock_post_json.return_value = mock_response


    fetcher = DummyFetcher(
        client_id="fake",
        client_secret="fake",
        coord_json_path=str(coords_path),
        out_path=str(output_file)
    )

    result = fetcher.fetch()

    assert result == str(output_file)
    assert output_file.exists()
    assert output_file.read_bytes() == b"fake data"
    mock_fetch_auth_token.assert_called_once()
    mock_load_bbox.assert_called_once()
    mock_post_json.assert_called_once()
