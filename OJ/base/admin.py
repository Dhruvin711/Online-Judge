from django.contrib import admin

# Register your models here.

from .models import Problem, TestCases, Solution

admin.site.register(Problem)
admin.site.register(TestCases)
admin.site.register(Solution)