from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    name = 'Bob'
    context = {}
    context['name'] = name
    return render(request, 'home.html', context)

def about(request):
    context = {}
    context['name'] = 'About us'
    return render(request, 'about.html', context)
