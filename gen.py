#!/usr/bin/env python3

assert __name__ == "__main__"

import glob
import os
import os.path
import shutil
import subprocess

from jinja2 import Environment, FileSystemLoader

SRC_DIR = "src"
SCSS_SRC = os.path.join(SRC_DIR, "stylesheets", "main.scss")
OUT_DIR = "out"
CSS_OUT = os.path.join(OUT_DIR, "css", "main.css")

# Delete old output directory
print("Delete old output directory (if present)")
try:
    shutil.rmtree(OUT_DIR)
except FileNotFoundError:
    pass

# Make new output directory
print("Make new output directory")
os.mkdir(OUT_DIR)

# Compile SCSS
print("Render SCSS")
os.makedirs(os.path.dirname(CSS_OUT), exist_ok=True)
args = [
    "scss",
    SCSS_SRC,
    CSS_OUT,
]
subprocess.run(args).check_returncode()

# Load Templates
print("Load Jinja templates")
env = Environment(loader=FileSystemLoader(SRC_DIR))

# Render index.html
print("Render and write index.html")
open("out/index.html", "w").write(env.get_template("data/index.jinja").render())
