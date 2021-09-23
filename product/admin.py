from django.contrib import admin
from .models import Product, Category, ProductType, ProductSpecification, ProductSpecificationValue, ProductImageTable
from mptt.admin import MPTTModelAdmin
from django import forms

# Register your models here.

# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ["title", "quantity", "slug", "price", "in_stock", "created"]
#     prepopulated_fields = {"slug": ("title", )}
#     list_filter = ["in_stock"]
#     list_editable = ["price", "in_stock"]
#
#
# class CategoryModelAdmin(admin.ModelAdmin):
#     list_display = ["category_name", "slug"]
#     prepopulated_fields = {"slug": ("category_name", )}
#
#
# admin.site.register(Product, ProductModelAdmin)
# admin.site.register(Category, CategoryModelAdmin)

admin.site.register(Category, MPTTModelAdmin)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImageTable


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]






















