#!/usr/bin/env python3

import os
import os.path
import shutil
import subprocess
import markdown
from collections import defaultdict

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


class DataFile:

    def __init__(self, path):
        self.input_data = open(path).read()
        self.__output_data = None

        self.path = path
        self.filename = os.path.basename(path)
        parts = self.filename.split('.')
        self.untagged_filename = parts[0]
        self.tags = parts[1:-1]
        self.ext = parts[-1]

        if self.ext == "mkd":
            self.input_type = 'markdown'
            self.output_ext = 'html'
        else:
            self.input_type = 'raw'
            self.output_ext = self.ext

        output_filename = self.untagged_filename + '.' + self.output_ext
        dirname = os.path.dirname(path)
        self.output_path = os.path.join(
                out_dir,
                dirname[len(data_dir) + 1:],
                output_filename)

    @property
    def output_data(self):
        if self.__output_data is None:
            if self.ext == "mkd":
                self.__output_data = md.convert(self.input_data)
            else:
                self.__output_data = self.input_data
        return self.__output_data


def get_data_dict():
    out = defaultdict(get_data_dict)
    return out


def split_path(path):
    path, filename = os.path.split(path)
    path_parts = [filename]
    while path != '':
        path, filename = os.path.split(path)
        path_parts.insert(0, filename)
    return path_parts


class SiteData:

    def __init__(self):
        self.__root = get_data_dict()

    def add(self, path):
        '''Loads the specified file and adds it to the collection.'''
        f = DataFile(path)

        f_dir = self.nav_tree(f.path)
        f_dir[f.filename] = f

    def nav_tree(self, path):
        '''Navigates the virtual directory tree to find the dict containing a
        file.'''
        path_parts = split_path(path)
        loc = self.__root
        for part in path_parts[:-1]:
            loc = loc[part]
        return loc

    def get(self, path):
        '''Retrieves the specified file from the collection or raises a
        KeyError.'''
        # TODO optimize this so it doesn't make a ton of extra dicts when we
        # don't find the desired path
        f_dir = self.nav_tree(path)
        filename = os.path.basename(path)
        v = f_dir[filename]
        if isinstance(v, DataFile):
            return v
        else:
            raise KeyError(path)

    def __iter__(self):
        def walk():
            stack = []
            current = iter(self.__root.items())
            try:
                while True:
                    try:
                        filename, contents = next(current)
                        if isinstance(contents, DataFile):
                            yield contents
                        # Look at the child directory contents
                        elif len(contents) > 0:
                            stack.append(current)
                            current = iter(contents.items())
                    # Finished with the current iterator
                    except StopIteration:
                        current = stack.pop()
            # Nothing else in the stack
            except IndexError:
                pass
        return walk()


site_data = SiteData()

# Copy data directory
for root, dirs, files in os.walk(data_dir):
    for f in files:
        path = os.path.join(root, f)
        site_data.add(path)
for f in site_data:
    print('Writing', f.path, 'to', f.output_path)
    os.makedirs(os.path.dirname(f.output_path), exist_ok=True)
    open(f.output_path, mode='w').write(f.output_data)

# Compile SCSS
print("Compile SCSS:", stylesheet)
os.makedirs(os.path.dirname(out_stylesheet), exist_ok=True)
subprocess.check_call(["sass", stylesheet, out_stylesheet])
print("\tOk")
