from django.urls import path

from .views import StayListView

urlpatterns = [
    path('/list', StayListView.as_view()),
]