from unittest import mock

from django.test import RequestFactory, TestCase

from app_products.views import index, search, substitutes


class ViewsUnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.name = 'a'

        class MockObject:
            def __init__(self):
                self.id = 123
                self.product_name = 'test product name'
                self.nutriscore = 'e'

        self.test_product = MockObject()

    def test_index(self):
        request = self.factory.get('/')
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Du gras, oui, mais de', str(response.content))

    def test_search(self):
        request = self.factory.get('/search')
        request.method = 'POST'
        with mock.patch(
            'app_products.views.FoodProductsManager.'
            'find_matching_food_products_to',
            return_value=[self.test_product],
        ):
            response = search(request)
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                ('<a href="/substitutes/' + str(self.test_product.id))
                and ('class="card-link">' + self.test_product.product_name),
                str(response.content),
            )

    def test_substitutes(self):
        request = self.factory.get('/substitutes/999')
        request.method = 'POST'
        with mock.patch(
            'app_products.views.FoodProductsManager.' 'find_product_by_id',
            return_value=[self.test_product],
        ):
            with mock.patch(
                'app_products.views.FoodProductsManager.'
                'find_substitutes_to',
                return_value=[self.test_product],
            ):
                response = substitutes(request, 999)
                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    ('href="/product_details/' + str(self.test_product.id))
                    and ('aliment">' + self.test_product.product_name),
                    str(response.content),
                )
