from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import ToDo

User = get_user_model()  # Get the custom user model

class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
                model = User
                fields = ['username', 'email', 'password']

	def create(self, validated_data):
        	# Hash the password before saving the user
		validated_data['password'] = make_password(\
						validated_data['password'])
		return super().create(validated_data)

class ToDoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ToDo
		fields = ['id', 'title', 'description']
