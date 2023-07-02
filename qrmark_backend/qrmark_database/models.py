from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    
    def get_short_name(self):
        return self.user_id


class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=100)
    level = models.IntegerField()
    
    def __str__(self):
        return self.student.user_id
    

class Lecturer(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.lecturer.user_id

class Course(models.Model):
    course = models.CharField(max_length=100)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='courses_taught')
    level = models.IntegerField()
    students = models.ManyToManyField(Student, related_name='courses_enrolled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.course
    
    class Meta:
        ordering = ['-created_at']
    
class QrCode(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='qrcodes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='qrcodes')
    qr_code = models.ImageField(upload_to='qr_codes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.qr_code.url
    
    class Meta:
        ordering = ['-created_at']
    
class Attendance(models.Model):
    student = models.ManyToManyField(Student)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    qr_code = models.ForeignKey(QrCode, on_delete=models.CASCADE, related_name='attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.course.course
    
    class Meta:
        ordering = ['-created_at']
