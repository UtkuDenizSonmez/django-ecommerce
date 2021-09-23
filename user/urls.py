from django.contrib.auth.tokens import default_token_generator
from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from .forms import LoginForm, PwdResetForm, PwdResetConfirmForm

app_name = "user"

urlpatterns = [
    # Registering
    path("register/", views.register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>", views.activate_account, name="activate"),
    # Login & Logout
    path("login/", auth_views.LoginView.as_view(template_name="user/login.html", form_class=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/user/login/"), name="logout"),
    # Dashboard(orders)
    path("dashboard/", views.dashboard, name="dashboard"),
    # Address
    path("addresses/", views.view_addresses, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:public_id>", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:public_id>", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:public_id>", views.set_default, name="set_default"),
    # Editing Profile
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/delete/", views.delete_profile, name="delete_profile"),
    path("profile/delete_confirmation/",
         TemplateView.as_view(template_name="user/delete-confirmation.html"),
         name="delete_confirmation"),
    # Changing Password (Using django's built-in views)
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="user/password/password_reset_form.html",
        success_url="password_reset_email_confirm",
        email_template_name="user/password/password_reset_email.html",
        token_generator=default_token_generator,
        form_class=PwdResetForm), name="password_reset"),
    # path("", include("django.contrib.auth.urls")),  # reverse for password_reset_complete
    path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(
        template_name="user/password/password_reset_confirm.html",
        success_url=reverse_lazy("user:password_reset_complete"),
        form_class=PwdResetConfirmForm), name="password_reset_confirm"),
    path("password_reset/password_reset_email_confirm/",
         TemplateView.as_view(template_name="user/password/reset_status.html"), name="password_reset_done"),
    path("password_reset_complete/",
         TemplateView.as_view(template_name="user/password/reset_status.html"), name="password_reset_complete"),
    # Wishlist
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:product_id>", views.add_to_wishlist, name="add_to_wishlist"),
]
