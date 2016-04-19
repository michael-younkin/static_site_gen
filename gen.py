#!/usr/bin/env python3

import os
import os.path
import shutil

assert __name__ == "__main__"

src_dir = "src"
data_dir = os.path.join(src_dir, "data")
out_dir = "out"

try:
    shutil.rmtree(out_dir)
except FileNotFoundError:
    pass

os.mkdir(out_dir)

for root, dirs, files in os.walk(data_dir):
    for f in files:
        path = os.path.join(root, f)
        dest = os.path.join(out_dir, path[len(data_dir) + 1:])
        print("Copying", os.path.join(root, f), "to", dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(path, dest)
