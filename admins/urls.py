from django.urls import path

from admins.views import AdminStayView

urlpatterns = [
    path('/<int:admin_id>', AdminStayView.as_view()),
]
