instructions = [


        # Blog Posts
        ("build_template",
            ("markdown", ("glob", "data/blog/*.mkd")),
            "blog.jinja"
        ),
        # Blog Index
        ("build_template", "data/blog/index.jinja"),
        # Root index
        ("build_template", "data/index.jinja"),
        # Stylesheet
        ("scss", "stylesheets/main.scss", "css/main.css"),
]
