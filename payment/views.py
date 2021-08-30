import json
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

from basket.basket import Basket
from orders.views import payment_confirmation
import stripe
import os
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

# Create your views here.


@login_required
def payment_details(request):
    basket = Basket(request)
    total = str(basket.total_price())
    total = total.replace(".", "")
    total = int(total)

    stripe.api_key = env("STRIPE_SECRET_KEY")
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='USD',
        metadata={'userid': request.user.id}
    )

    return render(request, "payment/payment-details.html", {"basket": basket, "client_secret": intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)

    if event.type == "payment_intent.succeeded":
        payment_confirmation(event.data.object.client_secret)
    else:
        print(f"Unhandled event type {event.type}")

    return HttpResponse(status=200)


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "payment/order-placed.html")


