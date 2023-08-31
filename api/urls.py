from django.urls import path
from knox import views as knox_views

from . import views

app_name = "api"

# authentication
urlpatterns = [
    path("", views.OverviewAPI.as_view(), name="overview"),
    path("login/", views.LoginAPI.as_view(), name="login"),
        # logout user
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # logout user from all sessions
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

# others
urlpatterns += [
    path("courses/", views.CRUDCourse.as_view(), name="courses"),
    path("delete-course/", views.DeleteCourseAPI.as_view(), name="delete_courses"),
    path("delete-all-courses/", views.DeleteAllCoursesAPI.as_view(), name="delete_all_courses"),
    path("students/", views.CRUDStudent.as_view(), name="students"),
    path("delete-student/", views.DeleteStudentAPI.as_view(), name="delete-student"),
    path("codes/", views.CRUDCodeAPI.as_view(), name="codes"),
    path('attendance/', views.TakeAttendanceAPI.as_view(), name='attendance'),
]