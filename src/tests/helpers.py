def test_file_at(path, content):
    with open(path, "w") as file:
        file.write(content)