from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	username = models.CharField(max_length=20, unique=True, blank=False)
	password = models.CharField(max_length=200, blank=False)
	referer = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
	points = models.IntegerField(default=0)
	referal_code = models.CharField(max_length=60, default=0)

	def __str__(self):
		return self.username
