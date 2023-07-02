from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 
urlpatterns = [
    path('auth/student/login/', views.StudentLoginAPI.as_view()),
    path('auth/lecturer/login/', views.LecturerLoginAPI.as_view()),
    path('dashboard/lecturer/generate-qr-code/', views.GenerateQrCodeAPI.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)