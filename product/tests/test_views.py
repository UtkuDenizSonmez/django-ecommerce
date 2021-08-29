from unittest import skip
from django import test
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from ..models import Product, Category
from django.urls import reverse
from product.views import home

# Create your tests here.

# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#     def text_skip_example(self):
#         pass


class test_url_allowed_hosts(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(category_name="watch", slug="watch")
        User.objects.create(username="admin")
        self.data1 = Product.objects.create(
            category_id=1, 
            created_by_id=1, 
            title="apple watch", 
            price=99, 
            slug="apple watch",
            image="watch-image.png"
            )

    def test_url_allowed_hosts(self):
        """
            Test allowed hosts
        """
        response = self.c.get("/", HTTP_HOST="mydomain.com")
        self.assertEqual(response.status_code, 400)
        res = self.c.get("/", HTTP_HOST="yourdomain.com")
        self.assertEqual(res.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(reverse("product:detail", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_search_category_url(self):
        response = self.c.get(reverse("product:search_category", args=["watch"]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = home(request)
        html = response.content.decode("utf-8")
        # print(html)
        self.assertIn("<title> Home </title>", html) 
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))   
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get("/1")
        response = home(request)
        html = response.content.decode("utf-8")
        self.assertIn("<title> Home </title>", html) 
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))   
        self.assertEqual(response.status_code, 200)
