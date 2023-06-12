from django.urls import path
from . import views 
urlpatterns = [
    path('auth/student/login/', views.StudentLoginAPI.as_view()),
    path('auth/lecturer/login/', views.LecturerLoginAPI.as_view())
]