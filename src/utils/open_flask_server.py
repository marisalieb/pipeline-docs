from pathlib import Path
import os
import subprocess
import signal
import psutil
import time
import sys

SERVER_SCRIPT = Path(__file__).parent / "server.py"
PID_FILE = Path(__file__).parent / "flask_server.pid"

def kill_old_server():
    """Kill any existing Flask server process."""
    try:
        pid = int(PID_FILE.read_text().strip())
        if psutil.pid_exists(pid):
            os.kill(pid, signal.SIGTERM)
            time.sleep(1)
    except Exception:
        pass
    PID_FILE.unlink(missing_ok=True)

def start_new_server(data_folder: str):
    """
    Start server pointing to the user-selected data folder, folder is needed for saving the coorinates later on.
    
    Args:
        data_folder (str): Path to the data folder.
    """
    kill_old_server()
    print(f"Starting Flask server with data folder: {data_folder}")
    proc = subprocess.Popen([sys.executable, str(SERVER_SCRIPT), data_folder], preexec_fn=os.setsid)
    PID_FILE.write_text(str(proc.pid))

