from django.db import models
# from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Problem(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    topic_tag = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TestCases(models.Model):
    input = models.TextField()
    output = models.TextField()
    
