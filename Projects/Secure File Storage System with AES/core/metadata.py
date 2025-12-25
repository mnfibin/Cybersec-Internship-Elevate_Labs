import json
import os


def save_meta(meta, path):
    with open(path + ".meta", "w") as f:
        json.dump(meta, f)


def load_meta(path):
    return json.load(open(path + ".meta"))
