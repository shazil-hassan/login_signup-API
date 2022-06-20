
from dataclasses import field
import email
from wsgiref import validate
from rest_framework import serializers
from  .models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        password=serializers.CharField(style={'input_type':'password'}, write_only=True,validators=[validate_password])
        password2=serializers.CharField(style={'input_type':'password'},write_only=True)
        
        model=User
        fields=['username','email','password','password2','phone','age']
        # extra_kwargs={'password':{'write_only':True}}

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2 :
            raise serializers.ValidationError("Password does not match")
        return attrs   

    def create(self, validated_data):
        try:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                age=validated_data['age']
            )

        
            user.set_password(validated_data['password'])
            user.save()

            return user
        except Exception as e:
            return e
            
                


class Studentlogin_Serializer(serializers.ModelSerializer):
    class Meta:
        # email=serializers.EmailField()
        model=User
        fields=['email', 'password']


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField()
    class Meta:
        field=['email']
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            # print( uid)
            token=PasswordResetTokenGenerator().make_token(user)
            # print(token)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            # print(link)
            return attrs

 