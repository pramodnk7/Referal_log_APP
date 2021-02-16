from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from .models import UserProfile
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from .sendemail import send_mail




class userLogin(APIView):
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


class userSignUp(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'signuppage.html'
	def get(self, request):
		logout(request)
		referal_code = request.GET.get('referal_code') if request.GET.get('referal_code') else 0
		return Response({'referal_code':referal_code})

	def post(self, request, *args, **kwargs):
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

def userLogout(request):
	try:
		logout(request)
	except Exception as e:
		pritn(e, flush=True)
	return redirect("/login/")


def dashboard(request):
	try:
		if not request.user.is_authenticated:
			return redirect("/login/")
		user_profile = UserProfile.objects.get(user__username=request.user)
		return render(request, 'dashboardpage.html', {"user_profile":user_profile})
	except Exception as e:
		print(e, flush=True)
		return redirect("/signup/")


def generateRefcode(request):
	response = {'status': 0, 'error_info':'Internal Error'}
	try:
		user_profile = UserProfile.objects.get(user__username=request.user)
		referal_code = datetime.now().strftime("%H%m%S%d%M%Y")
		response['status'] = 1
		response['referal_code'] = referal_code+str(user_profile.id)
		user_profile.referal_code = response['referal_code']
		user_profile.save()
		print(referal_code, flush=True)
	except Exception as e:
		print(e, flush=True)
	return HttpResponse(json.dumps(response))


def sendRefCodeEmail(request):
	response = {'status': 0, 'error_info':'Internal Error'}
	try:
		if not request.user.is_authenticated:
			response['error_info'] = 'Please refresh the page and try again'
		else:
			user_profile = UserProfile.objects.get(user=request.user)
			body = """Hi,<br>{} has sent the referal code.<br> 
					Please <a href="http://127.0.0.1:8000/signup/?referal_code={}">Click here</a> to Sign Up.""".format(user_profile.user.username, user_profile.referal_code)
			send_mail("Referal code from "+user_profile.user.username, body, request.POST.get('email'))
			response['status'] = 1
	except Exception as e:
		raise e
	return HttpResponse(json.dumps(response))