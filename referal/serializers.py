from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'points', 'referal_code', 'password',)
		write_only_fields = ('password',)


	def validate(self, attrs):
		if User.objects.filter(username=attrs['username']).exists():
			raise serializers.ValidationError({'username', ('Username already exists')})
		self.referalcode = str(attrs.get('referalcode', 0))
		if self.referalcode != "0":
			self.referer = User.objects.filter(referal_code=self.referalcode)
			if not self.referer:
				raise serializers.ValidationError({'referalcode', ('Invalid referal code')})
		return super().validate(attrs)


	def create(self, validated_data):
		print(self.referalcode, 'referalcode', flush=True)
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		if self.referalcode != "0":
			user.referer = self.referer[0]
			user.points = 100
			self.referer[0].points += 100
			user.save()
			self.referer[0].save()
		return user