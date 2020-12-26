import httpx
import json
import pathlib
import re
import os
from datetime import datetime

root = pathlib.Path(__file__).parent.resolve()
TOKEN = os.environ['TODOIST_TOKEN']


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(
        marker, chunk, marker)
    return r.sub(chunk, content)


def replace_chunk_no_space(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->`{}`<!-- {} ends -->".format(
        marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_todos():
    url = "https://api.prod.ashish.me/todos".format(
        TOKEN)
    todos = httpx.get(url).json()

    tasks = []

    for todo in todos:
        if not todo['completed']:
            tasks.append(todo)

    return tasks[::-1]


def fetch_completed():
    url = "https://api.prod.ashish.me/todos".format(
        TOKEN)
    todos = httpx.get(url).json()

    tasks = []

    for todo in todos:
        if todo['completed']:
            tasks.append(todo)

    return tasks[::-1]


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    todos = fetch_todos()
    todos_md = "\n".join(
        [
            "- {title}".format(
                title=todo["content"].strip().capitalize(),
            )
            for todo in todos
        ]
    )
    rewritten = replace_chunk(readme_contents, "todos", todos_md)

    completed = sorted(
        fetch_completed(),
        key=lambda x: datetime.fromisoformat(x["completedDate"].split("T")[
                                            0]), reverse=True
    )[:15]
    completed_md = "\n".join(
        [
            "* {title} - *{date}*".format(
                title=todo["content"].strip().capitalize(),
                date=datetime.fromisoformat(todo["completedDate"].split("T")[
                                            0]).strftime("%b %d %Y")
            )
            for todo in completed
        ]
    )
    rewritten = replace_chunk(rewritten, "completed", completed_md)
    readme.open("w").write(rewritten)
