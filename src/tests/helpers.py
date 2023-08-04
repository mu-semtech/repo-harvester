from os.path import exists, dirname
from os import mkdir


def test_file_at(path, content):
    dir = dirname(path)
    if dir is not "" and not exists(dir):
        mkdir(dir)
    with open(path, "w") as file:
        file.write(content)