from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

# Create your models here.


# class Category(models.Model):
#     category_name = models.CharField(max_length=250, db_index=True)
#     slug = models.CharField(max_length=250, unique=True)
#
#     class Meta:
#         verbose_name_plural = "Categories"
#
#     def get_absolute_url(self):
#         return reverse("product:search_category", kwargs={"slug": self.slug})
#
#     def __str__(self):
#         return self.category_name
#
#
# class ProductManager(models.Manager):  # Listing only if is_active == True
#     def get_queryset(self):
#         return super(ProductManager, self).get_queryset().filter(is_active=True)
#
#
# class Product(models.Model):
#     GENDER_CHOICES = [("M", "MALE"), ("F", "FEMALE")]
#
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     description = models.TextField()
#     image = models.ImageField(upload_to="images/", default="images/default.png")
#     slug = models.CharField(max_length=250)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     quantity = models.IntegerField(default=1)
#     gender = models.CharField(default="MAN", choices=GENDER_CHOICES, max_length=5)
#     in_stock = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()
#     products = ProductManager()
#
#     class Meta:
#         verbose_name_plural = "Products"
#         verbose_name = "Product"
#         ordering = ("-created", )
#
#     def get_absolute_url(self):
#         return reverse("product:detail", kwargs={"slug", self.slug})
#
#     def __str__(self):
#         return self.title
#

class Category(MPTTModel):
    """
    Category model implemented with MPTT
    """
    category_name = models.CharField(
        verbose_name=_("Category name"),
        help_text=_("Unique and Required"),
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"),
        max_length=255,
        unique=True
    )
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["category_name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("product:search_category", kwargs={"slug": self.slug})

    def __str__(self):
        return self.category_name


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types of products that are for sale.
    """
    name = models.CharField(verbose_name=_("Product name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    The ProductSpecification Table contains product specification or features for product types.
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)  # So you can't delete any ProductType
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The Product Table contains all product items.
    """
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_("Title"), help_text=_("Required"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    gender = models.CharField(default="M", choices=GENDER_CHOICES, max_length=5)
    quantity = models.IntegerField(default=1)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99")
            },
        },
        max_digits=5,
        decimal_places=2
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99")
            },
        },
        max_digits=5,
        decimal_places=2
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ("-created_at", )
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    """
    The ProductSpecificationValue Table holds each of the products individual specification or bespoke features.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product specification value (maximum of 255 words)"),
        max_length=255
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImageTable(models.Model):
    """
    The product image table
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative Text"),
        help_text=_("Please add an alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


# class CustomerWishlist(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_product")
#     customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist_customer")

