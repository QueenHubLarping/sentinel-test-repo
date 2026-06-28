from django.urls import path

from checkout.views import checkout

urlpatterns = [
    path("checkout", checkout, name="checkout"),
]
