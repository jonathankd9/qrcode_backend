# django
from django.shortcuts import render
from django.contrib.auth import login
from qrmark_database.models import Course, Student, UniqueCode
from api.serializers import CodesSerializer, CourseSerializer, StudentSerializer, UserSerializer

# rest framework
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

# knox
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView


class OverviewAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "The API for TickTrack is running successfully",
            "endpoints": [
                {"endpoint": "/", "description": "returns the overview of the entire api infrastructure"}, #noqa
                {"endpoint": "/login", "description": "used to login the user"}, # noqa
                {"endpoint": "/logout","description": "used to logout the current user from the current device"}, # noqa
                {"endpoint": "/logoutall", "description": "used to logout current user from all devices"}, # noqa
                {"endpoint": "/courses", "description": "Used to get, create, update and delete courses"}, # noqa
                {"endpoint": "/delete-course", "description": "Used to delete courses"}, # noqa
                {"endpoint": "/delete-all-course", "description": "Used to delete all courses"}, # noqa
                {"endpoint": "/students", "description": "Used to get, create, update and delete students"}, # noqa
                {"endpoint": "/codes", "description": "Used to get, create, update and delete codes"}, # noqa
            ]
        })


class LoginAPI(KnoxLoginView):
    '''For handling user logins'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        '''Uses the post method to login the user'''
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        # Delete token - this will logout any other users using this account
        AuthToken.objects.filter(user=user).delete()
        return Response({
            "message": "Login Successful",
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_200_OK)


class CRUDCourse(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''Used to get all courses created by user'''
        courses = Course.objects.filter(lecturer=request.user)
        return Response({
            "courses": CourseSerializer(courses, many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Used to create a new course'''
        course_code = request.data.get("course_code")
        course_name = request.data.get("course_name")
        course = Course.objects.filter(course_code=course_code).first() # noqa
        # check for duplicate course code
        if course is not None:
            return Response({
                "message": "Course Code Already Exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        # create new course
        obj = Course.objects.create(
            course_code=course_code,
            course_name=course_name,
            lecturer=request.user
        )
        return Response({
            "message": "Course Created Successfully",
            "course": CourseSerializer(obj).data
        }, status=status.HTTP_201_CREATED)
        
        
    def put(self, request,*args, **kwargs):
        '''Used to update a course'''
        user = request.user
        course_id = request.data.get("course_id")
        course_code = request.data.get("course_code")
        course_name = request.data.get("course_name")
        obj = Course.objects.filter(id=course_id, lecturer=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Course Fot Found"
            }, status=status.HTTP_404_NOT_FOUND)
        # check if course belongs to user
        obj.course_code = course_code
        obj.course_name = course_name
        obj.save()
        return Response({
            "message": "Course Updated Successfully",
            "course": CourseSerializer(obj).data
        }, status=status.HTTP_200_OK)
        
    def delete(self, request, *args, **kwargs):
        '''Used to delete a course'''
        user = request.user
        course_id = request.data.get("course_id")
        obj = Course.objects.filter(id=course_id, lecturer=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Course Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response({
                "message": "Course Deleted Successfully",
            }, status=status.HTTP_200_OK)



class DeleteCourseAPI(APIView):
    '''Used to delete a course'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''Used to delete a course'''
        user = request.user
        course_id = request.data.get("course_id")
        obj = Course.objects.filter(id=course_id, lecturer=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Course Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response({
                "message": "Course Deleted Successfully",
            }, status=status.HTTP_200_OK)


class DeleteAllCoursesAPI(APIView):
    '''Used to delete all courses'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''Used to delete all courses created by lecturer'''
        user = request.user
        courses = Course.objects.filter(lecturer=user)
        # check of course exists
        if len(courses) == 0:
            return Response({
                "message": "No Courses Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            courses.delete()
            return Response({
                "message": "Courses Deleted Successfully",
            }, status=status.HTTP_200_OK)


class CRUDStudent(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''Used to get all students created by user'''
        studnets = Student.objects.filter(created_by=request.user)
        return Response({
            "students": StudentSerializer(studnets, many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Used to create a new course'''
        course_id = request.data.get("course_id")
        student_id = request.data.get("student_id")
        student_name = request.data.get("student_name")
        student_level = request.data.get("student_level")
        course = Course.objects.filter(id=course_id, lecturer=request.user).first() # noqa
        if course is None:
            return Response({
                "message": "Course Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        obj = Student.objects.create(
            student_id=student_id,
            student_name=student_name,
            student_level=student_level,
            created_by=request.user
        )
        # add student to course
        course.students.add(obj)
        
        return Response({
            "message": "Student Created Successfully",
            "student": StudentSerializer(obj).data
        }, status=status.HTTP_201_CREATED)
        
        
    def put(self, request,*args, **kwargs):
        '''Used to update a course'''
        user = request.user
        student_pk = request.data.get("student_pk") # primary key
        student_id = request.data.get("student_id")
        student_name = request.data.get("student_name")
        student_level = request.data.get("student_level")
        obj = Student.objects.filter(id=student_pk, created_by=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Student Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        # check if course belongs to user
        obj.student_id = student_id
        obj.student_name = student_name
        obj.student_level = student_level
        obj.save()
        return Response({
            "message": "Student Updated Successfully",
            "student": StudentSerializer(obj).data
        }, status=status.HTTP_200_OK)
        

class DeleteStudentAPI(APIView):
    '''Used to delete a student'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''Used to delete a student'''
        user = request.user
        student_id = request.data.get("student_id")
        obj = Student.objects.filter(student_id=student_id, created_by=user).first()
        # check of course exists
        if obj is None:
            return Response({
                "message": "Student Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response({
                "message": "Student Deleted Successfully",
            }, status=status.HTTP_200_OK)



class CRUDCodeAPI(APIView):
    '''Used to create and get unique codes'''
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        '''Used to get all unique codes created by user'''
        print(request.user)
        codes = UniqueCode.objects.filter(course__lecturer=request.user)
        return Response({
            "codes": CodesSerializer(codes, many=True).data
        }, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        # get user
        user = request.user
        # get course code, date and time
        course_code = request.data.get("course_code")
        # valid_date = request.data.get("valid_date")
        # start_time = request.data.get("start_time")
        # end_time = request.data.get("end_time")
        # get course
        course = Course.objects.filter(lecturer=user, code=course_code).first() # noqa
        # check if course exists
        if course is None:
            return Response({
                "message": "Course Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        # get students
        students = course.students.all()
        if len(students) == 0:
            return Response({
                "message": "Add Students to Course First"
            }, status=status.HTTP_400_BAD_REQUEST)
        unique_codes = []
        # create unique codes
        for student in students:
            obj = UniqueCode(
                course=course,
                valid_date=valid_date,
                start_time=start_time,
                end_time=end_time
            )
            unique_codes.append(obj)
        # save unique codes
        UniqueCode.objects.bulk_create(unique_codes)
        return Response({
            "message": f"{len(unique_codes)} Codes Generated Successfully"
        }, status=status.HTTP_201_CREATED)
        # return unique codes
        

class TakeAttendanceAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        student_id = request.data.get("student_id")
        code = request.data.get("code")
        attendance_code = UniqueCode.objects.filter(code=code).first()
        if attendance_code is None:
            return Response({
                "message": "Code Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        course = attendance_code.course
        # chceck if student is in course
        student = Student.objects.filter(student_id=student_id, course=course).first() # noqa
        if student is None:
            return Response({
                "message": "Student Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
       