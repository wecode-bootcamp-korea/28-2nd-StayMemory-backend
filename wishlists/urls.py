from django.urls import path

from wishlists.views import WishlistView

urlpatterns = [
    path('', WishlistView.as_view()),
]
