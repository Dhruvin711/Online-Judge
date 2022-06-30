from django.shortcuts import render
from django.http import HttpResponse
from .models import Problem, TestCases
from django.db.models import Q

# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    problems = Problem.objects.filter(
        Q(name__icontains = q) |
        Q(topic_tag__icontains = q)
    )
    context = {'problems':problems}

    return render(request, 'base/home.html', context)

def problemPage(request, pk):
    problem = Problem.objects.get(id=pk)
    context = {'problem':problem}

    return render(request, 'base/problem-page.html', context)