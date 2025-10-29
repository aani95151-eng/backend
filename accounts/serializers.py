from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
class ResisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required =False)
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    


    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        
        return data
   

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()  # ← Add this line!

        return user  
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Invalid username or password")
        
        user = User.objects.get(username=data['username'])
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid username or password")
        
        return data
    def get_jwt_token(self, data):
       user = authenticate(
            username=data['username'],
            password=data['password'],

            )
       if not user:
           return {'message ':'invalied credent','data' : {}}
       
       refresh = RefreshToken.for_user(user)
       return {'message ':'login successfull','data' : {'token ' :{'refresh' : str(refresh),'access' : str(refresh.access_token)}}}