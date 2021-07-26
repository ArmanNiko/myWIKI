import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from . import util
from django.urls import reverse

import markdown2
from random import choice

def convert(file, name):
    text = file
    html = markdown2.markdown(text)
    new = 'encyclopedia\\templates\\encyclopedia'

    with open(f"{name.replace('md', 'html').replace('entries', new)}", 'w') as f:
        f.write(html)
    
    return f"{name.replace('md', 'html').replace('entries', new)}"

class CreatePage(forms.Form):
    title = forms.CharField(label="title", max_length=20, min_length=3)
    content = forms.CharField(label="content", min_length=30, widget=forms.Textarea)
def index(request):
    return render(request, "encyclopedia\\index.html", {
        "entries": util.list_entries(),
        "random": choice(util.list_entries())
    })

def show(request, title=""):
    if request.method == 'POST':
        title = request.POST.get("q")
    try:
        return render(request, convert(*util.get_entry(title)))
    except:
        if title == 'index.html':
            return HttpResponseRedirect(reverse('wiki:index'))

        new = []
        for entry in util.list_entries():
            if title.lower() in entry.lower():
                new.append(entry)
        if len(new) == 0:
            return render(request, 'encyclopedia\\notfound.html', {
                'entries': util.list_entries(),
            })

        return render(request, 'encyclopedia\\searched.html', {
            'entries': new,
        })

def create(request, title):
    mode = ''
    if request.method == 'POST':
        form = CreatePage(request.POST)
        if form.is_valid():
            titl = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if titl in util.list_entries() and title == 'created':
                return render(request, 'encyclopedia\\create.html', {
                    'form': form,
                    'mode': 'This Page already exists',
                })
            
            if titl not in util.list_entries() and title == 'edited':
                return render(request, 'encyclopedia\\create.html', {
                    'form': form,
                    'mode': 'This Page does not exist',
                })

            if f'<title>{titl}</title>' not in content:
                content = f'<title>{titl}</title>\n' + content
            if f'#{titl}' not in content:
                content = f'#{titl}\n' + content
            if not content.endswith('[Home Page](index.html)'):
                content += f'\n[Edit this Page]({titl.replace(" ", "_")}+create)\n[Home Page](index.html)'
            util.save_entry(titl, content)
            return render(request, convert(*util.get_entry(titl)))

    else:
        title = title.replace('_', ' ')
        if title == 'new':
            mode = 'Create a New Page'
            form = CreatePage()
            form.fields['content'].initial = 'You can use HTML and Markdown in writing the content if you want.'
        elif title in util.list_entries():
            mode = 'Edit a Page'
            form = CreatePage()
            form.fields['title'].initial = title
            form.fields['content'].initial = util.get_entry(title)[0]
        else:
            return render(request, 'encyclopedia\\notfound.html', {
                'entries': util.list_entries(),
            })
        
        return render(request, 'encyclopedia\\create.html', {
            'form': form,
            'mode': mode,
        })
        
        
