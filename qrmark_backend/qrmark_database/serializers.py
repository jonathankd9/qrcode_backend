from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User,Student, Lecturer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id','first_name', 'last_name', 'other_names','password','is_student','is_lecturer']
        
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        user_id = data.get("user_id", "")
        password = data.get("password", "")
        
        if not user_id:
            raise serializers.ValidationError("The User ID must be set")
        
        if not user_id.isdigit() or len(user_id) != 8:
            raise serializers.ValidationError("The User ID must be exactly 8 digits")

        if password is None or len(password) != 5 or not password.isdigit():
            raise serializers.ValidationError("The password must be exactly 5 digits")
        
        return data

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student', 'course', 'lecturer', 'level']

class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['lecturer', 'course']

class StudentLoginSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=8)
    pin = serializers.CharField(max_length=5, write_only=True)
    
    def validate(self, data):
        student_id = data.get("student_id")
        password = data.get("pin")
        user = authenticate(request=self.context.get("request"), user_id=student_id, password=password)
        if not user:
            raise serializers.ValidationError("Unable to login with provided credentials")
        if not user.is_student:
            raise serializers.ValidationError("Unable to login with provided credentials") 
        data["user"] = user
        return data
        
class LecturerLoginSerializer(serializers.Serializer):
    lecturer_id = serializers.CharField(max_length=8)
    pin = serializers.CharField(max_length=5, write_only=True)
    
    def validate(self, data):
        lecturer_id = data.get("lecturer_id")
        password = data.get("pin")
        user = authenticate(request=self.context.get("request"), user_id=lecturer_id, password=password)
        if not user:
            raise serializers.ValidationError("Unable to login with provided credentials")
        if not user.is_lecturer:
            raise serializers.ValidationError("Unable to login with provided credentials") 
        data["user"] = user
        return data
        