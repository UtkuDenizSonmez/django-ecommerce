from django.shortcuts import render, get_object_or_404
from .basket import Basket

from django.http import JsonResponse
from product.models import Product


def cart_items(request):
    basket = Basket(request)
    return render(request, "cart.html", {"basket": basket})


def add_item_to_basket(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product_qty = int(request.POST.get('productQuantity'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, quantity=product_qty)

        response = JsonResponse({"data": "test"})
        return response


def remove_item(request):
    basket = Basket(request)
    if request.POST.get('action') == 'delete':
        product_id = request.POST.get('productId')
        basket.remove(product=product_id)

        response = JsonResponse({"data": "delete"})
        return response
