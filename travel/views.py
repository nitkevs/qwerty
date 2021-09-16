from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    name = 'Bob'
    context = {}
    context['name'] = name
    return render(request, 'home.html', context)
