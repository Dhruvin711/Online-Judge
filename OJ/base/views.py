from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
import os, filecmp
# import subprocess

from .models import Problem, TestCases, Solution

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

    if request.method == 'POST':
        code = request.FILES['solution']
        
        with open('/Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/code-01.cpp', 'wb+') as dest:
            for chunk in code.chunks():
                dest.write(chunk)

        os.system('g++ /Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/code-01.cpp')
        os.system('./a.out < /Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/input.txt > /Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/output.txt')

        out1 = '/Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/output.txt'  
        out2 = '/Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/oj_output.txt'   

        if filecmp.cmp(out1, out2, shallow=False):
            verdict = 'Accepted'
        else:
            verdict = 'Wrong Answer'

        # if subprocess.call(["gcc", code]) == 0:
        #     subprocess.call(['./a.out < /Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/input.txt > /Users/dhruv/Desktop/Web Development/Websites/Online-Judge-Static/output.txt'])
        #     verdict = 'Accepted'
        # else:
        #     verdict = 'Wrong Answer'

        solution = Solution()
        solution.verdict = verdict
        solution.problem = Problem.objects.get(pk=pk)
        solution.submitted_time = timezone.now()
        # solution.save()

        context = {'solution':solution}

        return render(request, 'base/solution.html', context)
        
    return render(request, 'base/problem-page.html', context)

# def submitProblem(request, pk):

#     return HttpResponse('')