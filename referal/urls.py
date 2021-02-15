from django.urls import path, include
from .views import UserLogin, signUp, UserLogout, dashboard, registerUser,generateRefcode, sendRefCodeEmail

urlpatterns = [
    path('login/', UserLogin.as_view() ),
    path('signup/', signUp),
    path('register-user/', registerUser),
    path('logout/', UserLogout),
    path('dashboard/', dashboard),
    path('generate-ref-code/', generateRefcode),
    path('send-ref-code-email/', sendRefCodeEmail),
]
