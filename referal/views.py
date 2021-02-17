from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
import json
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from .sendemail import send_mail
from .serializers import UserSerializer
from .models import User
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



class userLogin(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'loginpage.html'
	def get(self, request):
		if request.user.is_authenticated:
			return redirect("/dashboard/")
		return Response({})

	def post(self, request, *args, **kwargs):
		response = {'status':0, 'error_info':'Internal Error.'}
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
		if not user:
			response['error_info'] = "Invalid username or password."
			return Response(response, status=status.HTTP_200_OK)
		else:
			login(request, user)
			response['status'] = 1
		return Response(response, status=status.HTTP_201_CREATED)


class userSignUp(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	serializer_class = UserSerializer
	template_name = 'signuppage.html'
	def get(self, request):
		logout(request)
		referal_code = request.GET.get('referal_code') if request.GET.get('referal_code') else 0
		return Response({'referal_code':referal_code})

	def post(self, request, *args, **kwargs):
		try:
			serializer = UserSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
			else:
				return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
		except Exception as e:
			print(e, flush=True)
		return Response({'status':1}, status=status.HTTP_201_CREATED)

def userLogout(request):
	try:
		logout(request)
	except Exception as e:
		print(e, flush=True)
	return redirect("/login/")


def dashboard(request):
	try:
		if not request.user.is_authenticated:
			return redirect("/login/")
		user = User.objects.get(username=request.user)
		return render(request, 'dashboardpage.html', {"user_profile":user})
	except Exception as e:
		print(e, flush=True)
		return redirect("/signup/")


def generateRefcode(request):
	response = {'status': 0, 'error_info':'Internal Error'}
	try:
		user_profile = User.objects.get(username=request.user)
		referal_code = datetime.now().strftime("%H%m%S%d%M%Y")
		response['status'] = 1
		response['referal_code'] = referal_code+str(user_profile.id)
		user_profile.referal_code = response['referal_code']
		user_profile.save()
		print(referal_code, flush=True)
	except Exception as e:
		print(e, flush=True)
	return HttpResponse(json.dumps(response))



class sendRefCodeEmail(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, format=None):
		user_profile = User.objects.get(username=request.user.username)
		body = """Hi,<br>{} has sent the referal code.<br> 
				Please <a href="http://127.0.0.1:8000/signup/?referal_code={}">Click here</a> to Sign Up.""".format(user_profile.username, user_profile.referal_code)
		send_mail("Referal code from "+user_profile.username, body, request.POST.get('email'))
		return Response({'status':1}, status=status.HTTP_200_OK)

