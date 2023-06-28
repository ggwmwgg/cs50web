from django.db import IntegrityError
from .models import Entry


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    titles = list(Entry.objects.values_list('title', flat=True))
    if len(titles) == 0:
        default_entries()
        titles = list(Entry.objects.values_list('title', flat=True))
        return titles
    return titles


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    try:
        post = Entry(title=title, content=content)
        post.save()
    except IntegrityError:
        post = Entry.objects.get(title=title)
        post.content = content
        post.save()


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        content = Entry.objects.get(title=title)
        return content.content
    except Entry.DoesNotExist:
        return None


def default_entries():
    """
    Creates default entries
    """
    print("Creating default entries")
    post = Entry(title="CSS", content="# CSS\nCSS is a language that can be used to add style to an [HTML](/wiki/HTML) page.")
    post.save()

    post = Entry(title="Django", content="# Django\nDjango is a web framework written using [Python](/wiki/Python) that allows for the design of web applications that generate [HTML](/wiki/HTML) dynamically.")
    post.save()

    post = Entry(title="Flask", content="# Flask\nFlask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.")
    post.save()

    post = Entry(title="Git", content="# Git\nGit is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.")
    post.save()

    post = Entry(title="HTML", content="# HTML\nHTML is a markup language that is used to create web pages.")
    post.save()

    post = Entry(title="Python", content="# Python\nPython is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant indentation.")
    post.save()
