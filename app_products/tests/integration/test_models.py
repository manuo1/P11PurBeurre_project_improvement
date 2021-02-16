from django.test import TestCase

from app_products.models import FoodCategory, FoodProduct


class TestModels(TestCase):
    def setUp(self):

        self.test_category = FoodCategory.objects.create(
            category_name='test_category'
        )
        self.test_product = FoodProduct.objects.create(
            product_name='test_product_name',
            nutriscore='e',
            barcode='123',
            image_url='https://static.openfoodfacts.org/test_image.jpg',
            energy_kj='123',
            energy_kcal='123',
            protein='123',
            glucid='123',
            lipid='123',
            fiber='123',
            salt='123',
        )

    def test_foodcategory_model_str_method(self):
        self.assertEquals(
            str(self.test_category), self.test_category.category_name
        )

    def test_foodproduct_model_str_method(self):
        self.assertEquals(
            str(self.test_product), self.test_product.product_name
        )
