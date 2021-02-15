from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	referer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
	points = models.IntegerField(default=0)
	referal_code = models.CharField(max_length=60, default=0)

	def __str__(self):
		return self.name +"( "+user.username +" )"
