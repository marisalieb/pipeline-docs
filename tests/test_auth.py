import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from utils.auth import fetch_auth_token

@patch("utils.auth.requests.post")
def test_fetch_token_success(mock_post): 

    mock_response = MagicMock()
    mock_response.status_code = 200 # sim a successful response
    mock_response.json.return_value = {"access_token": "mock_token"} # sims a json response
    mock_post.return_value = mock_response 

    token = fetch_auth_token("fake_id", "fake_secret")
    assert token == "mock_token"
    mock_post.assert_called_once()

@patch("utils.auth.requests.post")
def test_fetch_token_failure(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 401 # mock unauthorized response
    mock_post.return_value = mock_response

    token = fetch_auth_token("bad_id", "bad_secret")
    assert token is None
    mock_post.assert_called_once()
