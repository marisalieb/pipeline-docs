
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from utils.delete_images import delete_existing_images

def create_temp_file(dir_path, filename):
    path = dir_path / filename
    path.write_text("test")
    return path

def test_delete_existing_images_deletes_matching_files(tmp_path):
    file1 = create_temp_file(tmp_path, "prefix_1.jpg")
    file2 = create_temp_file(tmp_path, "prefix_2.jpg")
    file3 = create_temp_file(tmp_path, "other_1.jpg")

    delete_existing_images(tmp_path, "prefix", "jpg")

    assert not file1.exists()
    assert not file2.exists()
    assert file3.exists()

