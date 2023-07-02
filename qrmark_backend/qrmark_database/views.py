from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import authenticate
from .serializers import *
from .models import *
import time
import random
from datetime import datetime
from qrcode import make
from django.core.files.base import ContentFile
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404

class StudentLoginAPI(generics.GenericAPIView):
    serializer_class = StudentLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        student_id = serializer.validated_data["student_id"]
        pin = serializer.validated_data["pin"]
        
        user = authenticate(request=self.request, user_id=student_id, password=pin)
        
        if user is None or not user.is_student:
            response_data = {
                "message": "Invalid credentials",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
        response_data = {
            "message": "Login successful",
            "data": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(response_data, status=status.HTTP_200_OK)


class LecturerLoginAPI(generics.GenericAPIView):
    serializer_class = LecturerLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        lecturer_id = serializer.validated_data["lecturer_id"]
        pin = serializer.validated_data["pin"]

        user = authenticate(request=self.request, user_id=lecturer_id, password=pin)
        
        if user is None or not user.is_lecturer:
            response_data = {
                "message": "Invalid credentials",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
        response_data = {
            "message": "Login successful",
            "data": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class GenerateQrCodeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        lecturer = request.user
        if not lecturer.is_lecturer:
            response_data = {
                "message": "Only lecturers can generate QR codes",
                "data": None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = QRCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        lecturer = serializer.validated_data["lecturer"]
        course = serializer.validated_data["course"]
        
        # Generate a unique dynamic data for the QR code
        timestamp = int(time.time())
        random_value = random.randint(1000, 9999)
        dynamic_data = f"{lecturer.id}_{course.id}_{timestamp}_{random_value}"
        
        qr_code = make(dynamic_data)

        # Create an in-memory file-like object to hold the image data
        image_io = io.BytesIO()
        qr_code.save(image_io, format='PNG')

        # Create an InMemoryUploadedFile from the in-memory file-like object
        image_file = InMemoryUploadedFile(
            image_io,
            None,
            'qr_code.png',
            'image/png',
            len(image_io.getvalue()),
            None
        )

        serializer.save(qr_code=image_file)
        
        response_data = {
            "message": "QR code generated successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class ScanQRCodeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QRCodeScanSerializer
    
    def post(self, request):
        student = request.user
        if not student.is_student:
            response_data = {
                "message": "Only students can scan QR codes",
                "data": None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Retrieve the student information from the request data
        student_id = request.data.get('student_id')
        qr_code_id = request.data.get('qr_code_id')

        # Retrieve the student, course, and QR code instances
        student = get_object_or_404(Student, student_id=student_id)
        qr_code = get_object_or_404(QrCode, id=qr_code_id)
        course = qr_code.course

        # Check if the student is registered for the course
        if not student.is_registered_for_course(course):
            response_data = {
                'message': 'Student is not registered for this course.',
                'data': None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Mark attendance for the student
        attendance = Attendance.objects.create(student=student, course=course, qr_code=qr_code)

        response_data = {
            'message': 'Attendance marked successfully.',
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
