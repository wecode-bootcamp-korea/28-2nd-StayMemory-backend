from django.urls import path

from reservations.views import ReservationInformationView

urlpatterns = [
    path('', ReservationInformationView.as_view()),
]
