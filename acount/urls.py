
from django.urls import path
from .views import *

urlpatterns = [
     path('stu_signup/', StudentSignup.as_view()),
    path('stu_login/', Studentlogin.as_view()),
    path('stu_profile/', UserProfileView.as_view()),
    path('stu_changepassword/', UserChangePasswordView.as_view()),
    # path('send-reset-password-email/', SendPasswordResetEmailView.as_view()),
    # path('reset-password/<uid>/<token>/', UseUserPasswordResetView.as_view()),

]