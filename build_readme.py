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
    url = "https://api.prod.ashish.me/todos"
    todos = httpx.get(url).json()

    tasks = []

    for todo in todos:
        if not todo['completed']:
            tasks.append(todo)

    return tasks[::-1]


def fetch_completed():
    url = "https://api.prod.ashish.me/todos"
    todos = httpx.get(url).json()

    tasks = []

    for todo in todos:
        if todo['completed']:
            tasks.append(todo)

    return tasks[::-1]


def fetch_stats():
    url = "https://api.prod.ashish.me/todos/stats"
    response = httpx.get(url).json()
    stats = {}

    for period, stat in response["short"].items():
        stats[period] = stat

    return stats


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    todos = fetch_todos()
    todos_md = "<br>".join(
        [
            "◻️  &nbsp; {title}".format(
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
    )[:20]
    completed_md = "<br>".join(
        [
            "✅  &nbsp; {title} - **_{date}_**".format(
                title=todo["content"].strip().capitalize(),
                date=datetime.fromisoformat(todo["completedDate"].split("T")[
                                            0]).strftime("%b %d %Y")
            )
            for todo in completed
        ]
    )
    rewritten = replace_chunk(rewritten, "completed", completed_md)

    stats = fetch_stats()
    week_md = "__Week__ - {stat}".format(
        stat=stats["week"][0],
    )
    rewritten = replace_chunk(rewritten, "week", week_md)
    month_md = "__Month__ - {stat}".format(
        stat=stats["month"][0],
    )
    rewritten = replace_chunk(rewritten, "month", month_md)
    year_md = "__Year__ - {stat}".format(
        stat=stats["year"][0],
    )
    rewritten = replace_chunk(rewritten, "year", year_md)

    readme.open("w").write(rewritten)
