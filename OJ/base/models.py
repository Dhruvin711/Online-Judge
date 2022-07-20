from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Problem(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    topic_tag = models.CharField(max_length=100, null=True)
    difficulty = models.CharField(max_length = 100, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Solution(models.Model):
    curr_user = models.CharField(max_length=100, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=100)
    submitted_time = models.DateTimeField()
    submitted_code = models.TextField()

    def __str__(self):
        return self.verdict
    
class TestCases(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
    input = models.TextField()
    output = models.TextField()

    def __str__(self):
        return self.problem.name