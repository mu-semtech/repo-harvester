from os.path import dirname, join

def stream_template(**context):
    app.update_template_context(context)
    #t = app.jinja_env.get_template(template_name)
    t = app.jinja_env.from_string("<html><body><ul>{% for item in progress %} <li>{{ item }}</li>{%- endfor %} </ul>  </body></html>")
    rv = t.stream(context)
    rv.enable_buffering(size=5)
    return rv
    

def get_template():
    with open(join(dirname(__file__), "stream_progress.html"), "r", encoding="UTF-8") as file:
        data = file.read()
    return data


def stream_progress(progress_iter):
    print("Meow")
    return app.response_class(stream_template(progress=progress_iter))
    

    