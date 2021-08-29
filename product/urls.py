from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:id>", views.detail, name="detail"),
    path("search/<slug:category_slug>/<str:gender>", views.search_category, name="search_category"),

]
