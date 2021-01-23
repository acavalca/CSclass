from django.shortcuts import render
from . import util
import random
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from django import forms

class NewEntryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Write Name Here"}),)
    body = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Write Markdown Body Here"}),)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "isIndex": True,
        "entries": util.list_entries(),
        "randomPage": random.choice(util.list_entries()),
    })

def search(request):
    searchWord = request.GET.get("q", "")
    partialsList = []
    isEmpty = True
    for entryTest in util.list_entries():
        if searchWord == entryTest:
            return HttpResponseRedirect(f"/wiki/{entryTest}")
        if searchWord in entryTest:
            partialsList.append(entryTest)
            isEmpty = False
        if partialsList == None:
            isEmpty = True

    return render(request, "encyclopedia/search.html", {
        "isIndex": True,
        "isEmpty": isEmpty,
        "randomPage": random.choice(util.list_entries()),
        "theList": partialsList,
    })

def editPage(request, entry):
    if request.method == "POST":
        newBody = request.POST.get("editBodyName", "")
        newName = "entries/" + entry + ".md"
        f = open(newName, "w")
        f.write(newBody)
        f.close()
        return HttpResponseRedirect(f"/wiki/{entry}")
    return render(request, "encyclopedia/edit.html", {
        "isIndex": True,
        "entry": entry,
        "entryBody": util.get_entry(entry),
        "randomPage": random.choice(util.list_entries()),
    })

def entry(request, entry):
    if util.get_entry(entry) != None:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "isIndex": False,
            "entry": entry,
            "entryBody": markdowner.convert(util.get_entry(entry)),
            "randomPage": random.choice(util.list_entries()),
         })

    else:
        return render(request, "encyclopedia/noEntry.html", {
            "isIndex": False,
            "randomPage": random.choice(util.list_entries()),
        })

def newPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            body = form.cleaned_data["body"]
            newName = "entries/" + name + ".md"
            try:
                f = open(newName, "x")
                f.write(body)
                f.close()
            except FileExistsError:
                return render(request, "encyclopedia/oldEntry.html", {
                    "isIndex": True,
                    "randomPage": random.choice(util.list_entries()),
                    "form": NewEntryForm()
                })
            return HttpResponseRedirect(f"/wiki/{name}")
    return render(request, "encyclopedia/newEntry.html", {
        "isIndex": True,
        "randomPage": random.choice(util.list_entries()),
        "form": NewEntryForm()
    })