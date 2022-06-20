
from wsgiref import validate
from rest_framework import serializers
from  .models import User
from django.contrib.auth.password_validation import validate_password


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
    class Meta:
        # email=serializers.EmailField()
        model=User
        fields=['email', 'password']