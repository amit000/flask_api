import json

cached_strings = {}
default_locale = "en-gb"


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as ft:
        cached_strings = json.load(ft)


def gettext(name):
    return cached_strings[name]


refresh()
