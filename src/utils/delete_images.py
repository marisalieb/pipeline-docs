from pathlib import Path

def delete_existing_images(folder_path, prefix, format):
    """
    Deletes images in the specified folder that match the given prefix/file name and format.

    Args:
        folder_path (str): The path to the folder containing images.
        prefix (str): The prefix/file name of the images to delete.
        format (str): The file format of the images to delete.
    """

    folder = Path(folder_path)
    pattern = f"{prefix}_*.{format}"
    images = list(folder.glob(pattern))
    
    if not images:
        print(f"No {format} images matching '{pattern}' found in {folder_path}.")
        return

    for image in images:
        try:
            image.unlink()
            print(f"Deleted: {image}")
        except Exception as e:
            print(f"Failed to delete {image}: {e}")
