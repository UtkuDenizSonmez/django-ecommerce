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
    phone = models.CharField(max_length=10, blank=True, unique=True, null=True)
    post_code = models.CharField(max_length=12, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="user/", default="user/default.png")
    # Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

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
