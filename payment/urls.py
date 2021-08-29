from django.contrib.auth.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("", views.payment_details, name="payment_details"),
    path("orderplaced/", views.order_placed, name="order_placed"),
    path("webhook/", views.stripe_webhook),
]
