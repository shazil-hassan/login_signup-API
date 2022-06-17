
from django.urls import path
from .views import Studentsignup, Studentlogin

urlpatterns = [
     path('stu_signup/', Studentsignup.as_view()),
    path('stu_login/', Studentlogin.as_view()),
]