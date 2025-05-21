from unittest.mock import patch, MagicMock
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from utils import open_flask_server

@patch("utils.open_flask_server.psutil.pid_exists", return_value=True)
@patch("utils.open_flask_server.os.kill")
@patch("utils.open_flask_server.time.sleep")
@patch("utils.open_flask_server.PID_FILE")
def test_kill_old_server(mock_pid_file, mock_sleep, mock_kill, mock_pid_exists):
    mock_pid_file.read_text.return_value = "12345"
    mock_pid_file.unlink = MagicMock()

    open_flask_server.kill_old_server()

    mock_pid_file.read_text.assert_called_once()
    mock_pid_exists.assert_called_once_with(12345)
    mock_kill.assert_called_once_with(12345, signal.SIGTERM)
    mock_sleep.assert_called_once()
    mock_pid_file.unlink.assert_called_once_with(missing_ok=True)
