from product.models import Product
from django.conf import settings


class Basket:
    """
        A base Basket class. 
        Providing some default behaviors that can be inherited or overrided as necessary.
    """
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}

        self.basket = basket

    def __iter__(self):
        """
            Making the basket iterable.
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = float(item["price"])
            yield item

    def __len__(self):
        """
            Returns the item count in basket.
        """
        return sum(item["quantity"] for item in self.basket.values())

    def add(self, product, quantity):
        """
            Adding and Updating the users basket session data
        """
        product_id = product.id
        if product_id not in self.basket:
            self.basket[product_id] = {"price": float(product.price), "quantity": quantity}
        else:
            self.basket[product_id]["quantity"] = quantity
        self.save()

    def remove(self, product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]

        self.save()

    def total_price(self):
        """
            Returns the total price of basket.
        """
        return sum(float(item["price"]) for item in self.basket.values())

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

        
