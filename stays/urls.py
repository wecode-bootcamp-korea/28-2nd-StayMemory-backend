from django.urls import path

from .views import StayListView

urlpatterns = [
    path('', StayListView.as_view()),
]