from django.urls import path, include
from .views import UserLogin, signUp, UserLogout, dashboard, registerUser

urlpatterns = [
    path('login/', UserLogin.as_view() ),
    path('signup/', signUp),
    path('register-user/', registerUser),
    path('logout/', UserLogout),
    path('dashboard/', dashboard),
]
