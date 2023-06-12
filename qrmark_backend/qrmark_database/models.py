from django.db import models

# Create your models here.

from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=8)
    pin = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=100)
    level = models.IntegerField()
