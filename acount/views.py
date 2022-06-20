
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import  generics

from .models import *
from .serializers import StudentSerializer,Studentlogin_Serializer
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class StudentSignup(generics.CreateAPIView):
     serializer_class = StudentSerializer
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



# class SendPasswordResetEmailView(APIView):

#     def post(self,request,format=None):
#         serializer=SendPasswordResetEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({'msg':'password reset link send your email Id'})
#         return Response({'msg':'InValid Information'})    
