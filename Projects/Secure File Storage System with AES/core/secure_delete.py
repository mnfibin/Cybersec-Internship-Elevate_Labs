import os
import random


def secure_delete(path):
    if not os.path.exists(path):
        return
    size = os.path.getsize(path)
    with open(path, "wb") as f:
        f.write(os.urandom(size))
    os.remove(path)
