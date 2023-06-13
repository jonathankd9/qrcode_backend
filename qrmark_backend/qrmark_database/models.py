from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

class User(AbstractBaseUser):
    user_id = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Configure the custom user manager
    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.user_id
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True



class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=100)
    level = models.IntegerField()

class Lecturer(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100, blank=True, null=True)