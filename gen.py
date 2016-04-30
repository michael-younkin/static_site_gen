#!/usr/bin/env python3

assert __name__ == "__main__"

from glob import glob
import os
import os.path
import shutil
import subprocess
from markdown import Markdown

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

# Load all blog posts
md = Markdown()

class BlogPost:

    def __init__(self, filename):
        self.filename = filename
        self.html = md.convert(open(filename).read())

blog_posts = {}
for blog_file in glob("src/data/blog/*.mkd"):
    blog_posts[blog_file] = BlogPost(blog_file)

# Make blog output directory
os.mkdir("out/blog")

# Render and save blog posts
for post in blog_posts.values():
    context = {"post_title": post.filename, "post_body": post.html}
    post_docs = env.get_template("templates/blog_post.jinja").render(context)
    name = os.path.splitext(os.path.basename(post.filename))[0]
    out_filename = "out/blog/%s.html" % name
    print("Render and write", out_filename)
    open(out_filename, "w").write(post_docs)
