from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.


def home(request):
    all_products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    # From DevToolbar is shows we are using extra query with .all().
    # But prefetch_related() we are not.

    paginator = Paginator(all_products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "count": paginator.count,
        "page": page_obj,
    }
    return render(request, "index.html", context=context)


def detail(request, id):
    selected_product = get_object_or_404(Product.objects.prefetch_related("product_image"), id=id)
    return render(request, "detail.html", {"requested_item": selected_product})


def search_category(request, category_slug, gender):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.prefetch_related("product_image").filter(category=category, gender=gender)

    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "selected-category.html", {"count": paginator.count, "page": page_obj})

