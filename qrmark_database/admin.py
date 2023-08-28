from django.contrib import admin
from .models import Student, Lecturer, User, QrCode, Course, Attendance, UniqueCode
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(QrCode)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(UniqueCode)
