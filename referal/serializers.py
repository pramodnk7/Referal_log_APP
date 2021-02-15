from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.response import Response


class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = ('name', 'points', 'user', 'referer')

	def save(self):
		if User.objects.filter(username=self.validate_data['email']).exists():
			return Response({'error_info':'User with email exists.'})
		user_profile = UserProfile()



class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=20, min_length=4, write_only=True)
	email = serializers.EmailField(max_length=100, min_length=4)
	name = serializers.CharField(max_length=100)
	