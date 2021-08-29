from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=250, db_index=True)
    slug = models.CharField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("product:search_category", kwargs={"slug": self.slug})

    def __str__(self):
        return self.category_name


class ProductManager(models.Manager):  # Listing only if is_active == True
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Product(models.Model):
    GENDER_CHOICES = [("M", "MALE"), ("F", "FEMALE")]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", default="images/default.png")
    slug = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=1)
    gender = models.CharField(default="MAN", choices=GENDER_CHOICES, max_length=5)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"
        ordering = ("-created", )

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug", self.slug})

    def __str__(self):
        return self.title
    
