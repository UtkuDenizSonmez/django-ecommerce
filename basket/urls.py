from django.urls import path
from . import views

app_name = "basket"

urlpatterns = [
    path("", views.cart_items, name="cart_items"),
    path("add/", views.add_item_to_basket, name="add_item_to_basket"),
    path("remove/", views.remove_item, name="remove_item_from_basket")
]
