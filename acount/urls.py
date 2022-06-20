
from django.urls import path
from .views import Studentsignup, Studentlogin,SendPasswordResetEmailView

urlpatterns = [
     path('stu_signup/', Studentsignup.as_view()),
    path('stu_login/', Studentlogin.as_view()),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view()),
]