from django.contrib import admin

# Register your models here.

from .models import User, Problem, TestCases

admin.site.register(User)
admin.site.register(Problem)
admin.site.register(TestCases)
