from unittest.mock import patch, ANY
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

@patch("utils.open_map.subprocess.Popen")
@patch("utils.open_map.Path.is_file")
@patch("builtins.print")
def test_open_map_file_exists(mock_print, mock_is_file, mock_popen):
    mock_is_file.return_value = True
    from utils import open_map
    open_map.open_map()
    mock_popen.assert_called_once()

@patch("utils.open_map.subprocess.Popen")
@patch("utils.open_map.Path.is_file")
@patch("builtins.print")
def test_open_map_file_missing(mock_print, mock_is_file, mock_popen):
    mock_is_file.return_value = False

    from utils import open_map
    open_map.open_map()

    mock_popen.assert_not_called()
    mock_print.assert_any_call(ANY)
