import os
import json

cached_strings = {}
default_locale = "en-gb"


def refresh():
    global cached_strings
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, f"..\\strings\\{default_locale}.json")
    with open(filename) as ft:
        cached_strings = json.load(ft)


def gettext(name):
    return cached_strings[name]


refresh()
