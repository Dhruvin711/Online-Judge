from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Problem, TestCases
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def loginPage(request):
    page = 'login'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorect')

    context = {'page':page}

    return render(request, 'base/login_page.html', context)

def logoutUser(request):
    logout(request)

    return redirect('login')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, 'An error occured during registration.')

    context = {'form':form}
    
    return render(request, 'base/login_page.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    problems = Problem.objects.filter(
        Q(name__icontains = q) |
        Q(topic_tag__icontains = q) |
        Q(difficulty__icontains = q)
    )
    context = {'problems':problems}

    return render(request, 'base/home.html', context)

def problemPage(request, pk):
    problem = Problem.objects.get(id=pk)
    context = {'problem':problem}

    return render(request, 'base/problem-page.html', context)