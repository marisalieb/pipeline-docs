import subprocess
from pathlib import Path

def open_map():
    """
    Open the map.html file in Firefox.
    This function checks if the file exists and opens it using the specified browser.
    """
    map_file = Path(__file__).parent / "map.html"
    firefox_path = "/usr/bin/firefox"

    if not map_file.is_file():
        print(f"Error: The file {map_file} does not exist.")
        return

    subprocess.Popen([firefox_path, str(map_file)])

if __name__ == "__main__":
    open_map()
