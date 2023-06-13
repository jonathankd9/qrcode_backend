from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .serializers import *

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