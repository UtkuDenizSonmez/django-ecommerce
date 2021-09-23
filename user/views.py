from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .forms import RegisterForm, EditForm, LoginForm, UserAddressForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

from .token import account_activation_token
from .models import UserBase, Address

from orders.views import user_orders
from product.models import Product
# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect("user:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.set_password(form.cleaned_data["password"])
            user.is_active = False  # Set this to True after email activation.
            user.save()

            # Email
            current_site = get_current_site(request)
            subject = "Activate Your Account!"
            message = render_to_string("user/registration/activation-email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                "token": account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse("Registered Successfully and Activation link sent. Please check your email.")
    else:
        form = RegisterForm()
    return render(request, "user/registration/register.html", {"form": form})

# Using Django's built-in views instead.
# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm()
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = UserBase.objects.filter(username=username)
#             if user.password == password and user.is_active:
#                 login(request, user)
#                 return redirect("product:home")
#             else:
#                 return redirect("user:login")


# Using Django's built-in views instead.
# @login_required
# def logout_user(request):
#     logout(request)
#     return redirect("product:home")


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("user:dashboard")
    else:
        return render(request, "user/registration/activation-invalid.html")


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "user/dashboard.html", {"orders": orders})


@login_required
def edit_profile(request):
    if request.method == "POST":
        current_user = UserBase.objects.get(username=request.user)
        form = EditForm(instance=current_user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EditForm(instance=request.user)
    return render(request, "user/edit-user.html", {"form": form})


@login_required  # Don't delete user details from database. Just set the is_active = False.
def delete_profile(request):
    user = UserBase.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("user:delete_confirmation")


# Addresses
@login_required
def view_addresses(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "user/address/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.save()
            return HttpResponseRedirect(reverse("user:addresses"))
    else:
        form = UserAddressForm()
    return render(request, "user/address/edit-address.html", {"form": form})


@login_required
def edit_address(request, public_id):
    if request.method == "POST":
        address = Address.objects.get(customer=request.user, pk=public_id)
        form = UserAddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("user:addresses"))
    else:
        address = Address.objects.get(customer=request.user, pk=public_id)
        form = UserAddressForm(instance=address)
    return render(request, "user/address/edit-address.html", {"form": form})


@login_required
def delete_address(request, public_id):
    address = Address.objects.get(customer=request.user, pk=public_id)
    address.delete()
    return redirect("user:addresses")


@login_required
def set_default(request, public_id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(customer=request.user, pk=public_id).update(default=True)
    return redirect("user:addresses")


@login_required
def wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)
    return render(request, "user/user-wishlist.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.error(request, "Removed " + product.title + " from your Wishlist")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your Wishlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




