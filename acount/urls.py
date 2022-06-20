
from django.urls import path
from .views import StudentSignup, Studentlogin

urlpatterns = [
     path('stu_signup/', StudentSignup.as_view()),
    path('stu_login/', Studentlogin.as_view()),
]