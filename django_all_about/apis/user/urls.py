
# django, drf lib
from django.urls import path

# app lib
from apis.user.views import RegisterAPIView, LoginAPIView, CustomTokenRefreshView

urlpatterns = [

    # 이메일로 회원가입
    path('register/', RegisterAPIView.as_view(), name='custom-register-apiview'),

    # 이메일로 로그인
    path('login/', LoginAPIView.as_view(), name='rest-auth-login-custom'),
    
    # 토큰 갱신
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh-apiview'),

]