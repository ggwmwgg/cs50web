import random as r
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .util import get_entry, list_entries, save_entry, default_entries


class NewPageForm(forms.Form):
    title = forms.CharField(
        label="title",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'id': 'title', 'name': 'title'})
    )
    content = forms.CharField(
        label="content",
        widget=forms.Textarea(attrs={'rows': 9, 'class': "form-control", 'name': "content", 'id': "content",
                                     'placeholder': "Enter content here"})
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })


def entry(request, title):
    get_content = get_entry(title)
    if get_content is None:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": get_content
        })


def search(request):
    query = request.GET.get('q')
    query = query.lower()
    list_e = list_entries()
    list_lower = [x.lower() for x in list_e]

    if query in list_lower:
        get_content = get_entry(query)
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": get_content
        })
    else:
        results = []
        for i in list_e:
            if query in i.lower():
                results.append(i)
        if not results:
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "found": False
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "found": True,
                "results": results
            })


def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            list_items = list_entries()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for i in list_items:
                if title.lower() == i.lower():
                    return render(request, "encyclopedia/add.html", {
                        "form": form,
                        "error": True
                    })
            save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewPageForm()
        })


def random(request):
    list_e = list_entries()
    random_entry = r.choice(list_e)
    return HttpResponseRedirect(reverse("entry", args=(random_entry,)))


def edit(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            save_entry(title, content)
            return HttpResponseRedirect(reverse("save", args=(request,)))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    else:
        content = get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": NewPageForm(initial={'title': title, 'content': content})
        })


def save(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            content = get_entry(form.cleaned_data["title"])
            return render(request, "encyclopedia/edit.html", {
                "form": NewPageForm(initial={'title': form.cleaned_data["title"], 'content': content})
            })
