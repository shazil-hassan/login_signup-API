

from importlib.resources import contents
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import  generics

from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created





def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class StudentSignup(generics.CreateAPIView):
    
    serializer_class = StudentSerializer
    def post(self,request,format=None):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Sign Up Successfully'})
        return Response({'msg':'InValid Information'})    

    # return Response({'token':token,'msg':'Login Successfully'})
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    
    # def post(self,request,format=None):
    #     serializer=StudentSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response({'msg':'Sign Up Successfully'})
    #     return Response({'msg':'InValid Information'})    

class Studentlogin(APIView):
    def post(self,request,format=None):
        serializer=Studentlogin_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Successfully'})
           
        return Response({'msg':'InValid Information'})


class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data)


class UserChangePasswordView(APIView):
    # permission_classes=[IsAuthenticated]
    # def post(self,request,format=None):
    #     serializer=UserChangePasswordSerializer(data=request.data,content={'user':'request.user'})
    #     if serializer.is_valid():
    #         return Response({'msg':'Password Change  Successfully'})
    
    permission_classes=[IsAuthenticated]

    def get_object(self, queryset=None):
            return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = UserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]})
                                
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'msg':'Password Change  Successfully'})

        return Response(serializer.errors)

# class SendPasswordResetEmailView(APIView):

#     def post(self,request,format=None):
#         serializer=SendPasswordResetEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
           
#             return Response({'msg':'password reset link send your email Id'})
#         return Response({'msg':'InValid Information'})    


# class UseUserPasswordResetView(APIView):
#     def post(self,request,uid,token,format=None):
#         serializer=UserPasswordResetSerializer(data=request.data,content={'uid':uid,'token':token})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'msg':'Password Change  Successfully'})



    
    @receiver(reset_password_token_created)
    
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
        """
        Handles password reset tokens
        When a token is created, an e-mail needs to be sent to the user
        :param sender: View Class that sent the signal
        :param instance: View Instance that sent the signal
        :param reset_password_token: Token Model Object
        :param args:
        :param kwargs:
        :return:
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}?token={}".format(
                instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
                reset_password_token.key)
        }

        # render email text
        email_html_message = render_to_string('email.html', context)
        # email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {title}".format(title="Some website title"),
            # message:
            email_html_message,
            # from:
            "shazilkazmi110@gmail.com",
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message)
        msg.send()

