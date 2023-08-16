from os.path import dirname, join

def get_template():
    with open(join(dirname(__file__), "stream_progress.html"), "r", encoding="UTF-8") as file:
        data = file.read()
    return data

send_to_html = ""
listening = False