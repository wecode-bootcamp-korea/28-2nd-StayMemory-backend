from django.urls import path

from users.views import SignInKakaoView

urlpatterns = [
    path('/signin-kakao', SignInKakaoView.as_view()),
]
