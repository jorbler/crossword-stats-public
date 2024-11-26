import os

PATH_DATA = "data/"
PATH_FIGURES = "figures/"

def check_directory(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)
    return