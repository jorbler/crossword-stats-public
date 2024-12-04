import os

PATH_DATA = "data/"
PATH_FIGURES = "figures/"

def check_directory(path: str) -> None:
    '''Checks if a directory exists and creates it if it doesn't.'''
    if not os.path.exists(path):
        os.mkdir(path)
    return