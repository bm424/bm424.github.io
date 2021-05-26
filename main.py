import glob
import markdown
import logging
import sys
import pathlib
import shutil
import collections
import dateutil.parser
from jinja2 import Environment, FileSystemLoader, select_autoescape

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

MarkdownFilePost = collections.namedtuple("MarkdownFilePost", ["title", "date", "html"])

def main():
    log.info("Starting")

    md = markdown.Markdown(extensions=["meta"])
    markdown_file_path_list = glob.glob("src/markdowns/*.md")
    markdown_file_name_list = [pathlib.Path(markdown_file_path).stem for markdown_file_path in markdown_file_path_list]

    if len(markdown_file_path_list) == 0:
        log.warning("No files found matching /app/src/*.md")

    log.info("Rendering markdown files...")

    markdown_file_post_list = []
    for markdown_file_path, markdown_file_name in zip(markdown_file_path_list, markdown_file_name_list):
        with open(markdown_file_path, "r") as markdown_file:
            markdown_file_content = markdown_file.read()
        markdown_file_html = md.convert(markdown_file_content)
        markdown_file_title = md.Meta.get("title", [None])[0]
        markdown_file_date = md.Meta.get("date", [None])[0]
        markdown_file_post = MarkdownFilePost(
            title=markdown_file_title,
            date=dateutil.parser.parse(markdown_file_date) if markdown_file_date else None,
            html=markdown_file_html,
        )
        markdown_file_post_list.append(markdown_file_post)
        with open(f"build/{markdown_file_name}.html", "w") as html_file:
            html_file.write(markdown_file_html)

    log.info("Rendering Index...")

    environment = Environment(
        loader=FileSystemLoader("src/templates"),
        autoescape=select_autoescape(),
    )

    index_template = environment.get_template("index.html")
    index_html = index_template.render(post_list=markdown_file_post_list)
    with open("build/index.html", "w") as index_file:
        index_file.write(index_html)

    log.info("Copying static assets...")
    static_file_list = glob.glob("src/static/*")
    for static_file in static_file_list:
        static_file_name = pathlib.Path(static_file).name
        shutil.copyfile(static_file, f"build/{static_file_name}")

    log.info("Finishing")


if __name__ == "__main__":
    main()
