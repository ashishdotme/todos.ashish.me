import httpx
import json
import pathlib
import re
import os
from pytz import timezone
import dateutil.parser as dt
from datetime import datetime
import ssl

ssl.SSLContext.verify_mode = ssl.VerifyMode.CERT_OPTIONAL
root = pathlib.Path(__file__).parent.resolve()

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
    url = "https://systemapi.prod.ashish.me/todos"
    todos = httpx.get(url).json()

    tasks = []

    for todo in todos:
        if not todo['completed']:
            tasks.append(todo)

    return tasks[::-1]


def fetch_completed():
    url = "https://systemapi.prod.ashish.me/todos"
    todos = httpx.get(url).json()

    tasks = []

    for todo in todos:
        if todo['completed']:
            tasks.append(todo)

    return tasks[::-1]


def fetch_stats():
    url = "https://systemapi.prod.ashish.me/todos/stats"
    return httpx.get(url).json()


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()

    todos = fetch_todos()
    todos_md = "<br>".join(
        [
            "◻️ &nbsp; {title}".format(
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
            "✅ &nbsp; {title} - **_{date}_**".format(
                title=todo["content"].strip().capitalize(),
                date=dt.parse(todo["completedDate"]).astimezone(timezone('Asia/Kolkata')).strftime("%b %d %Y")
            )
            for todo in completed
        ]
    )
    rewritten = replace_chunk(rewritten, "completed", completed_md)

    stats = fetch_stats()
    week_md = "<b>Current Week</b> - {stat} \n <b>Previous Week</b> - {stat2}".format(
        stat=len(stats["currentWeek"]), stat2=len(stats["previousWeek"]),
    )
    rewritten = replace_chunk(rewritten, "week", week_md, True)
    month_md = "<b>Current Month</b> - {stat} \n <b>Previous Month</b> - {stat2}".format(
        stat=len(stats["currentMonth"]), stat2=len(stats["previousMonth"]),
    )
    rewritten = replace_chunk(rewritten, "month", month_md, True)
    year_md = "<b>Current Year</b> - {stat} \n <b>Previous Year</b> - {stat2}".format(
        stat=len(stats["currentYear"]), stat2=len(stats["previousYear"]),
    )
    rewritten = replace_chunk(rewritten, "year", year_md, True)

    readme.open("w").write(rewritten)
