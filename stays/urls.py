from django.urls import path

from stays.views import (DetailPageView,
                         UnavailableDateView,
                         CalcPriceView,
                         StayListView)

urlpatterns = [
    path('', StayListView.as_view()),
    path('/<int:stay_id>', DetailPageView.as_view()),
    path('/<int:stay_id>/unavailable-date', UnavailableDateView.as_view()),
    path('/<int:stay_id>/price', CalcPriceView.as_view()),
]
