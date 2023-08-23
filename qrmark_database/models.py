from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from qrmark_backend.utils.enums import Gender, Level, Semester


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=8, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[(gender.value, gender.name) for gender in Gender], null=True, blank=True)
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
        return self.first_name
    
    def save(self, *args, **kwargs):
        # Combine the first_name, last_name, and other_names to create full_name
        if self.first_name and self.last_name:
            if self.other_names:
                self.full_name = f"{self.first_name} {self.other_names} {self.last_name}"
            else:
                self.full_name = f"{self.first_name} {self.last_name}"
        else:
            self.full_name = None

        super().save(*args, **kwargs)
    



class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=10, choices=[(level.value, level.name) for level in Level], blank=True, null=True)
    semester = models.CharField(max_length=10, choices=[(semester.value, semester.name) for semester in Semester], blank=True, null=True)
    
    def __str__(self):
        return self.student.user_id
    

class Lecturer(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    office = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.lecturer.user_id

class Course(models.Model):
    code = models.CharField(max_length=8, blank=True, null=True)
    title = models.CharField(max_length=100)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='courses_taught')
    level = models.IntegerField()
    students = models.ManyToManyField(Student, related_name='courses_enrolled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.code
    
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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    qr_code = models.ForeignKey(QrCode, on_delete=models.CASCADE, related_name='attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.course.course
    
    class Meta:
        ordering = ['-created_at']
