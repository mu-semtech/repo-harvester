# Package imports
from helpers import log
from flask import stream_with_context, Response
from threading import Thread
from time import sleep

"""Helper function to log to Docker & stream HTTP response"""


data = []
def info(string):
    global data
    log(string)
    log("@@")
    data.append(string)
    yield string

def stream():
    global data

    log("------------")
    log(data)
    log("@@@@@@@@@@@")
    for item in data:
        sleep(10)
        yield item


def response():
    log("a;@@€")
    thread = Thread(target=stream)
    thread.start()
    return Response(stream_with_context())

    
