#!/usr/bin/env python3

import os
import os.path
import shutil
import subprocess

assert __name__ == "__main__"

src_dir = "src"
data_dir = os.path.join(src_dir, "data")
stylesheet = os.path.join(src_dir, "stylesheets", "main.scss")
out_dir = "out"
out_stylesheet = os.path.join(out_dir, "css", "main.css")

try:
    shutil.rmtree(out_dir)
except FileNotFoundError:
    pass

os.mkdir(out_dir)

# Copy data directory
for root, dirs, files in os.walk(data_dir):
    for f in files:
        path = os.path.join(root, f)
        dest = os.path.join(out_dir, path[len(data_dir) + 1:])
        print("Copying", os.path.join(root, f), "to", dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(path, dest)

# Compile SCSS
os.makedirs(os.path.dirname(out_stylesheet), exist_ok=True)
subprocess.check_call(["sass", stylesheet, out_stylesheet])
