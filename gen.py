#!/usr/bin/env python3

import os
import os.path
import shutil
import subprocess
import markdown

assert __name__ == "__main__"

md = markdown.Markdown(extensions = ['markdown.extensions.meta'])

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
        print("File:", path)
        dest = os.path.join(out_dir, path[len(data_dir) + 1:])
        print("\tDest:", dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        ext = os.path.splitext(f)[1]
        if ext == ".mkd":
            print("\tParsing markdown")
            text = open(path).read()
            html = md.convert(text)
            open(dest, mode='w').write(html)
        else:
            print("\tCopying")
            shutil.copy(path, dest)

# Compile SCSS
print("Compile SCSS:", stylesheet)
os.makedirs(os.path.dirname(out_stylesheet), exist_ok=True)
subprocess.check_call(["sass", stylesheet, out_stylesheet])
print("\tOk")
