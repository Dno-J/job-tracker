import os

def ensure_folder(path: str) -> None:
    """
    Create the folder if it doesn't exist.

    Args:
        path (str): The directory path to ensure exists.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
