from django.urls import path, include
from .views import login, signin, signout, dashboard, registerUser

urlpatterns = [
    path('login/', login),
    path('signin/', signin),
    path('register-user/', registerUser),
    path('signout/', signout),
    path('dashboard/', dashboard),
]
