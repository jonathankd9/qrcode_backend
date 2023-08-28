# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from .manager import AccountManager

# from django.utils.crypto import get_random_string
# from datetime import datetime, time, date


# class User(AbstractBaseUser, PermissionsMixin):
#     staff_id = models.CharField(max_length=100, unique=True)
#     fullname = models.CharField(max_length=100, blank=True, null=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def get_fullname(self):
#         '''return the full name of the user'''
#         return self.fullname if self.fullname else self.staff_id if self.staff_id else 'Anonymous'  # noqa

#     objects = AccountManager()

#     USERNAME_FIELD = 'staff_id'

#     def __str__(self):
#         return self.get_fullname()

#     class Meta:
#         db_table = 'user'


# class Student(models.Model):
#     '''Model for creating and managing studnets'''
#     student_id = models.CharField(max_length=10)
#     student_name = models.CharField(max_length=200)
#     student_level = models.CharField(max_length=10)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.student_name


# class Course(models.Model):
#     '''Model for creating and managing courses'''
#     course_code = models.CharField(max_length=7)
#     course_name = models.CharField(max_length=200)
#     lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
#     students = models.ManyToManyField(Student, related_name="studnets")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.course_code + " " + self.course_name


# class UniqueCode(models.Model):
#     '''Models for generating and storing unique attendance codes'''
    
#     def generate_code() -> str:
#         allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
#         return get_random_string(length=5, allowed_chars=allowed_chars)

#     code = models.CharField(max_length=5, default=generate_code)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     valid_date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def is_expired(self) -> bool:
#         # Check if the current date and time are within the valid range
#         current_datetime = datetime.now()
#         current_date = current_datetime.date()
#         current_time = current_datetime.time()
        
#         if (current_date == self.valid_date) and (current_time >= self.start_time or current_time <= self.end_time ):
#             return False
#         else:
#             return True

#     def __str__(self) -> str:
#         return self.code


# class Attendance(models.Model):
#     '''Model for managing attendance'''
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     attendance_code = models.ForeignKey(UniqueCode, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.student.student_name
