instructions = [
        ("rmdir", "out"),
        ("mkdir", "out/css"),
        ("mkdir", "out/blog"),
        # Blog Posts
        ("apply", "build_with_template",
            ("flatten",
                "blog.jinja",
                ("apply", "markdown", ("glob", "data/blog/*.mkd"))
            ),
        ),
        # Blog Index
        ("build_template", "data/blog/index.jinja"),
        # Root index
        ("build_template", "data/index.jinja"),
        # Stylesheet
        ("scss", "stylesheets/main.scss", "css/main.css"),
]
