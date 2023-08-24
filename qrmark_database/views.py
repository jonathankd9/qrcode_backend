from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import authenticate
from .serializers import *
from .models import *
import time
import hashlib
import random
from datetime import datetime
from django.contrib.auth.hashers import make_password
from qrcode import make
from django.core.files.base import ContentFile
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

# For Student Login
class StudentLoginAPI(generics.GenericAPIView):
    serializer_class = StudentLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data["student_id"]
        pin = serializer.validated_data["pin"]
        # Authenticate the student
        user = authenticate(request=self.request, user_id=student_id, password=pin)

        if user is None or not user.is_student:
            response_data = {
                "message": "Invalid credentials",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Student instance corresponding to the authenticated user
        student = Student.objects.filter(student=user).first()

        if not student:
            response_data = {
                "message": "Student record not found",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Serialize the student information
        student_serializer = StudentSerializer(student)
        
        # Retrieve the courses the student is enrolled in
        courses = student.courses_enrolled.all()
        
        # Serialize the courses
        courses_serializer = CourseSerializer(courses, many=True)

        response_data = {
            "message": "Login successful",
            "data": {
                "user_info": UserSerializer(user, context=self.get_serializer_context()).data,
                "student_info": student_serializer.data,
                "courses": courses_serializer.data,
            },
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(response_data, status=status.HTTP_200_OK)

# For Lecturer Login
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
        
        # Retrieve the Lecturer instance corresponding to the authenticated user
        lecturer = Lecturer.objects.filter(lecturer=user).first()
        if not lecturer:
            response_data = {
                "message": "Lecturer record not found",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the lecturer information
        lecturer_serializer = LecturerSerializer(lecturer)
        
        # Retrieve the courses the lecturer teaches
        courses = lecturer.courses_taught.all()
    
        # Serialize the courses
        courses_serializer = CourseSerializer(courses, many=True)
         
        response_data = {
            "message": "Login successful",
            "data": {
                'user_info': UserSerializer(user, context=self.get_serializer_context()).data,
                'lecturer_info': lecturer_serializer.data,
                'courses': courses_serializer.data,
                     },
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(response_data, status=status.HTTP_200_OK)

# For QR Code Generation
# class GenerateQrCodeAPI(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         lecturer = request.user
#         if not lecturer.is_lecturer:
#             response_data = {
#                 "message": "Only lecturers can generate QR codes",
#                 "data": None,
#             }
#             return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = QRCodeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         lecturer = serializer.validated_data["lecturer"]
#         course = serializer.validated_data["course"]
#         qr_code_id = serializer.validated_data["id"]
#         print(qr_code_id)
        
#         # Generate a unique dynamic data for the QR code
#         timestamp = int(time.time())
#         random_value = random.randint(1000, 9999)
#         dynamic_data = f"{lecturer.lecturer.full_name}_{course.code}_{timestamp}_{random_value}"
        
#         qr_code = make(dynamic_data)

#         # Create an in-memory file-like object to hold the image data
#         image_io = io.BytesIO()
#         qr_code.save(image_io, format='PNG')

#         # Create an InMemoryUploadedFile from the in-memory file-like object
#         image_file = InMemoryUploadedFile(
#             image_io,
#             None,
#             'qr_code.png',
#             'image/png',
#             len(image_io.getvalue()),
#             None
#         )

#         serializer.save(qr_code=image_file)
        
#         response_data = {
#             "message": "QR code generated successfully",
#             "data": serializer.data,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

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
        dynamic_data = f"{lecturer.lecturer.full_name}_{course.code}_{timestamp}_{random_value}"
        
        # Compute a hash of the dynamic data as the QR code ID
        qr_code_id = hashlib.sha256(dynamic_data.encode()).hexdigest()

        # Include the QR code ID in the dynamic data
        dynamic_data_with_id = f"{qr_code_id}_{dynamic_data}"
        
        qr_code = make(dynamic_data_with_id)

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
            "data": serializer.data['qr_code']
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
# For QR Code Scanning
class ScanQRCodeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QRCodeScanSerializer
    
    def post(self, request):
        student = request.user
        if not student.is_student:
            response_data = {
                "message": "Only students can scan QR codes",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Retrieve the student information from the request data
        qr_code_id = request.data.get('qr_code_id')
        enrolled_student = Student.objects.filter(student=student).first()
        qr_code = QrCode.objects.filter(qr_code_id=qr_code_id).first()
        course = qr_code.course   
        
        # Check if the student is enrolled in the course
        if enrolled_student in course.students.all():
            # Mark attendance for the student
            Attendance.objects.create(student=enrolled_student, course=course, qr_code=qr_code)

            response_data = {
                'message': 'Attendance marked successfully.',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'message': 'Student is not enrolled in the course',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

