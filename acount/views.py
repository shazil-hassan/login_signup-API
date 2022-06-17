
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .models import *
from .serializers import StudentSerializer,Studentlogin_Serializer

# Create your views here.

class Studentsignup(APIView):

    def post(self,request,format=None):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Sign Up Successfully'})
        return Response({'msg':'InValid Information'})    

class Studentlogin(APIView):
    def post(self,request,format=None):
        serializer=Studentlogin_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                return Response({'msg':'Login Successfully'})
            else:
                return Response(serializer.errors)
        return Response({'msg':'InValid Information'})
