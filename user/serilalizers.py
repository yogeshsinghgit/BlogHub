# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)


    class Meta:
         model = CustomUser
         fields = ['username', 'email', 'password']


    def create(self, validated_data):
         user = CustomUser.objects.create_user(
              username = validated_data['username'],
              email = validated_data['email'],
              password = validated_data['password']
         )

         return user