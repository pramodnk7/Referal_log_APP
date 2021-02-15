from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.http.response import JsonResponse




# class login(APIView):
# 	renderer_classes = [TemplateHTMLRenderer]
# 	template_name = 'loginpage.html'

# 	def get(self, request):
# 		return Response({})


# class signin(APIView):
# 	renderer_classes = [TemplateHTMLRenderer]
# 	template_name = 'signinpage.html'

# 	def get(self, request):
# 		return Response({})
# 	@csrf_exempt
# 	def post(self, request, *args, **kwargs):
# 		serializer = UserProfileSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors)

def login(request):
	return render(request, 'loginpage.html', {})


def signin(request):
	referal_code = request.GET.get('referal_code')
	referal_code = referal_code if referal_code else 0
	return render(request, 'signinpage.html', {'referal_code':referal_code}) 


def registerUser(request):
	response = {'status': 0, 'error_info':'Internal error'}
	try:
		qd = request.POST
		if User.objects.filter(username=qd.get('email')).exists():
			response['error_info'] = 'User with email already exists. Please Login.'
		else:
			referal_code = qd.get('referal_code')
			if referal_code not in ["0", 0]:
				referal_code = str(referal_code)
				referer = UserProfile.objects.filter(referal_code=referal_code)
				if not referer:
					response['error_info'] = 'Invalid referal code.'
					return HttpResponse(json.dumps(response))
			user = User(username=qd.get('email'))
			user.set_password(qd.get('password'))
			user.save()
			user_profile = UserProfile(user=user)
			if referal_code not in ["0", 0]:
				referer = referer[0]
				user_profile.referer = referer
				user_profile.points = 100
				referer.points += 100
				referer.save()
			user_profile.save()
			response['status'] = 1
	except Exception as e:
		print(e, flush=True)
	return HttpResponse(json.dumps(response))

def signout(request):
	return HttpResponse("sign out")


def dashboard(request):
	return render(request, 'dashboardpage.html', {})

