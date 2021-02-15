from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout




class UserLogin(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'loginpage.html'
	def get(self, request):
		if request.user.is_authenticated:
			return redirect("/dashboard/")
		return Response({})

	def post(self, request, *args, **kwargs):
		response = {'status':0, 'error_info':'Internal Error.'}
		qd = request.data
		email = qd.get('email').strip() if qd.get('email') else qd.get('email')
		password = qd.get('password').strip() if qd.get('password') else qd.get('password')
		if not email or not password:
			response['error_info'] = "Email and password are mandatory."
			return HttpResponse(json.dumps(response))
		user = authenticate(username=email, password=password)
		if user is None:
			response['error_info'] = "Invalid Username(Email) or password."
			return HttpResponse(json.dumps(response))
		else:
			login(request, user)
			response['status'] = 1
			return HttpResponse(json.dumps(response))



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

# def login(request):
# 	return render(request, 'loginpage.html', {})


def signUp(request):
	logout(request)
	referal_code = request.GET.get('referal_code')
	referal_code = referal_code if referal_code else 0
	return render(request, 'signuppage.html', {'referal_code':referal_code}) 


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
			login(request, user)
	except Exception as e:
		print(e, flush=True)
	return HttpResponse(json.dumps(response))

def UserLogout(request):
	logout(request)
	return redirect("/login/")


def dashboard(request):
	try:
		if not request.user.is_authenticated:
			return redirect("/login/")
		user_profile = UserProfile.objects.get(user__username=request.user)
		return render(request, 'dashboardpage.html', {"user_profile":"user_profile"})
	except Exception as e:
		print(e, flush=True)
		return redirect("/login/")

