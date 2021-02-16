from django.urls import path, include
from .views import userLogin, userSignUp, userLogout, dashboard, generateRefcode, sendRefCodeEmail

urlpatterns = [
    path('login/', userLogin.as_view() ),
    path('signup/', userSignUp.as_view()),
    path('logout/', userLogout),
    path('dashboard/', dashboard),
    path('generate-ref-code/', generateRefcode),
    path('send-ref-code-email/', sendRefCodeEmail),
]
