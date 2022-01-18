from django.urls import path

from users.views import (SignInKakaoView,
                         UserInformationView)

urlpatterns = [
    path('/signin-kakao', SignInKakaoView.as_view()),
    path('/info', UserInformationView.as_view()),
]
