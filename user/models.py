import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get('is_staff'):
            raise ValueError('Superuser must be assigned to is_staff=True')
        if not kwargs.get('is_superuser'):
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email, username, password, **kwargs)

    def create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValueError(_("You must enter a valid email address."))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user


class UserBase(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250, blank=True)
    mobile = models.CharField(max_length=10, blank=True, unique=True, null=True)
    image = models.ImageField(upload_to="user/", default="user/default.png")
    # Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def email_user(self, subject, message):
        send_mail(subject, message, "sitename@email.com", [self.email])


class Address(models.Model):
    """
    Customer Address Table
    """
    public_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(UserBase, on_delete=models.CASCADE, verbose_name=_("Customer"))

    country_region = models.CharField(verbose_name=_("Country Region"), max_length=255)
    full_name = models.CharField(verbose_name=_("Full Name"), help_text=_("Required"), max_length=100)
    phone = models.CharField(verbose_name=_("Phone Number"), help_text=_("Required"), max_length=10)
    postcode = models.CharField(verbose_name=_("Post Code"), max_length=15, blank=True, null=True)
    address_line = models.CharField(verbose_name=_("Address Line 1"), help_text=_("Required"), max_length=255)
    address_line2 = models.CharField(verbose_name=_("Address Line 2"), help_text=_("Required"), max_length=255)
    town_base = models.CharField(verbose_name=_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(verbose_name=_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(verbose_name=_("Default"), default=False)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return "Address"

