
from asyncore import write
from dataclasses import field
import email
from lib2to3.pgen2 import token
from pyexpat import model
from tkinter.tix import Tree
from wsgiref import validate
from django.forms import ValidationError
from rest_framework import serializers

# from acount.ultis import util
from  .models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class StudentSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields=['username','email','password','confirm_password','phone','age']
        extra_kwargs={'confirm_password':{'write_only':True}, 'password':{'write_only':True}}
    

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def save(self):
        user = User(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            age=self.validated_data['age']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class Studentlogin_Serializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['email','password']



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username', 'email', 'phone', 'age']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        validate_password(value)
        return value

# class SendPasswordResetEmailSerializer(serializers.Serializer):
#     email=serializers.EmailField()
#     class Meta:
#         field=['email']
#     def validate(self,attrs):
#         email=attrs.get('email')
#         if User.objects.filter(email=email).exists():
#             user=User.objects.get(email=email)
#             uid=urlsafe_base64_encode(force_bytes(user.id))
#             # print( uid)
#             token=PasswordResetTokenGenerator().make_token(user)
#             # print(token)
#             link='http://localhost:3000/api/user/reset/'+uid+'/'+token
#             print(link)
#             data={
#                 'subject':'Reset Your Password',
#                 'body':'please click in this Link'+link,
#                 'to_email':user.email
#             }
#             util.send_email(data)
#             return attrs



# class UserPasswordResetSerializer(serializers.ModelSerializer):

#     password=serializers.CharField(style={'input_type':'password'},write_only=Tree)
#     password2=serializers.CharField(style={'input_type':'password'},write_only=Tree)

#     class Meta:
#         model=User
#         field=['password','password2']


#     def validate(self, attrs):
#         password=attrs.get('password')
#         password2=attrs.get('password2')
#         uid=self.context.get('uid')
#         token=self.context.get('token')
#         if password != password2:
#             raise serializers.ValidationError("password does not match")
#         id=smart_str( urlsafe_base64_decode(uid))
#         user=User.objects.get(id=id)
#         if not PasswordResetTokenGenerator().check_token(user,token):
#             raise ValidationError('token is invalid or expired')
#         user.set_password(password)
#         user.save()
#         return attrs()

 