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
subprocess.check_call(args)

# Load Templates
print("Load Jinja templates")
env = Environment(loader=FileSystemLoader(SRC_DIR))

# Render index.html
print("Render and write index.html")
open("out/index.html", "w").write(env.get_template("data/index.jinja").render())

# Load all blog posts
md = Markdown(extensions = ['markdown.extensions.meta'])

class BlogPost:

    def __init__(self, filename):
        self.filename = filename
        self.html = md.convert(open(filename).read())
        self.meta_data = md.Meta
        self.title = self.meta_data['title'][0]
        self.date = self.meta_data['date'][0]
        self.output_filename = "%s.html" % self.title
        self.output_path = "out/blog/%s" % self.output_filename
        self.index_href = self.output_filename
        self.root_href = "/blog/%s" % self.output_filename

blog_posts = {}
for blog_file in glob("src/data/blog/*.mkd"):
    blog_posts[blog_file] = BlogPost(blog_file)

# Make blog output directory
os.mkdir("out/blog")

# Render and save blog posts
for post in blog_posts.values():
    context = {"post_title": post.title, "post_body": post.html}
    post_docs = env.get_template("templates/blog_post.jinja").render(context)
    print("Render and write", post.output_path)
    open(post.output_path, "w").write(post_docs)

# Gen blog post index page
print("Render and write out/blog/index.html")
context = {"blog_posts": blog_posts.values()}
blog_index = env.get_template("templates/blog_index.jinja").render(context)
open("out/blog/index.html", "w").write(blog_index)
