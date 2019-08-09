from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'coreyms',
        'title': 'Django blog 1',
        'content': 'Lorem epsom...',
        'date_posted': 'August 28th, 2018'
    },
    {
        'author': 'janedoe',
        'title': 'Fashion blog 1',
        'content': 'Lorem epsom...',
        'date_posted': 'August 29th, 2018'
    },
]


def home(request):
    context = {
        'posts': posts,
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'about'})
