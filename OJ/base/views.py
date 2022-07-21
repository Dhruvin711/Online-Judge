from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import os, filecmp, sys
import subprocess

from .models import Problem, TestCases, Solution
from .forms import CreateUserForm

# Create your views here.

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
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
            
            messages.success(request, 'Logged in as ' + user.username)

            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorect')

    context = {'page':page}

    return render(request, 'base/login-page.html', context)

def logoutUser(request):
    logout(request)

    return redirect('login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            messages.success(request, 'Account is created for ' + user.username)

            return redirect('home')
        
        else:
            messages.error(request, 'An error occured during registration.')

    context = {'form':form}
    
    return render(request, 'base/register-page.html', context)

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

        with open("base/testcases/question-1/code.cpp", "wb+") as f:
            for chunk in code.chunks():
                f.write(chunk)
        f.close()

        # Code Execution

        command = "g++ base/testcases/question-1/code.cpp"
        subprocess.run(command, capture_output=True, check=True)

        p = TestCases.objects.filter(problem=problem)

        for i in range(len(p)):
            test_input = p[i].input
            test_output = p[i].output

            try:
                output = subprocess.run('a.exe', input = test_input, capture_output = True, text = True, check = True, timeout = 2)
            except subprocess.TimeoutExpired:
                verdict = "TLE"
                break

            test_output1 = "base/testcases/question-1/test_output.txt"
            with open(test_output1, "w") as f:
                f.write(test_output)
            f.close()
            
            output1 = "base/testcases/question-1/output-1.txt"
            with open(output1, "w") as f:
                f.write(output.stdout)
            f.close()
            
            if filecmp.cmp(output1, test_output1, shallow=False):
                verdict = 'Accepted'
                status = True
            else:
                verdict = 'Wrong Answer'
                break

        solution = Solution()
        solution.curr_user = request.user
        solution.verdict = verdict
        solution.problem = Problem.objects.get(pk=pk)
        solution.submitted_time = timezone.now()
        solution.submitted_code = open('base/testcases/question-1/code.cpp', 'r').read()
        solution.save()

        context = {'solution':solution}

        return render(request, 'base/solution.html', context)
        
    return render(request, 'base/problem-page.html', context)

def leaderboard(request):
    submissions = Solution.objects.all()

    context = {'submissions':submissions}

    return render(request, 'base/leaderboard.html', context)

def codePage(request, pk):
    submission = Solution.objects.get(id=pk)
    code = submission.submitted_code

    context = {'submission':submission, 'code':code}

    return render(request, 'base/code.html', context)