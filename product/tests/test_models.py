from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Product, Category

# Create your tests here.


class TestProduct(TestCase):
    def setUp(self):
        Category.objects.create(category_name="django")
        User.objects.create(username="admin")
        self.data1 = Product.objects.create(category_id=1, created_by_id=1, title="Django Test", price=99)

    def test_product_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "Django Test")


class TestCategory(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(category_name="test category", slug="test category")

    def test_category_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_name(self):
        data = self.data1
        self.assertEqual(str(data), "test category")

