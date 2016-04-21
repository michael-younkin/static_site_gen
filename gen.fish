#!/usr/bin/env fish

docker run -v (pwd):/main -t static_site_gen:latest /bin/sh -c "cd /main; ./gen.py"
