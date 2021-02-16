from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from app_products.models import FoodCategory, FoodProduct


class TestAppProductsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
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
        self.test_product.categories.add(self.test_category)
        self.test_user = self.User.objects.create_user(
            username='test_name',
            email='test_mail@mail.com',
            password='test_password',
        )
        self.search_form = {'search': self.test_product.product_name}
        self.login_data = {
            'username': 'test_name',
            'password': 'test_password',
        }

    """ index view Tests """

    def test_if_index_view_return_index_template(self):
        response = self.client.get(reverse('indexPage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    """ search view Tests """

    def test_if_search_get_method_return_search_template(self):
        response = self.client.get(reverse('search'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_if_search_view_post_method_return_matching_list(self):
        while FoodProduct.objects.count() < 20:
            new_product = FoodProduct.objects.get(pk=self.test_product.pk)
            new_product.barcode += FoodProduct.objects.count()
            new_product.pk = None
            new_product.save()
        response = self.client.post(reverse('search'), self.search_form)
        self.assertEquals(len(response.context['matching_list']), 9)
        self.assertTemplateUsed(response, 'search.html')

    """ substitutes view tests """

    def test_if_substitutes_view_return_substitutes_template(self):
        id = self.test_product.id
        response = self.client.get(reverse('substitutesPage', args=[id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitutes.html')

    def test_if_substitutes_view_return_404_if_no_product_to_substitute(self):
        id = FoodProduct.objects.latest('id').id + 1
        response = self.client.get(reverse('substitutesPage', args=[id]))
        self.assertEquals(response.status_code, 404)

    def test_if_substitutes_view_return_substitutes_list(self):
        while FoodProduct.objects.count() < 20:
            new_product = FoodProduct.objects.get(pk=self.test_product.pk)
            new_product.barcode += FoodProduct.objects.count()
            new_product.nutriscore = 'a'
            new_product.pk = None
            new_product.save()
            new_product.categories.add(self.test_category)
        id = self.test_product.id
        response = self.client.get(reverse('substitutesPage', args=[id]))
        self.assertEquals(len(response.context['substitutes_list']), 9)

    """ favorites view tests """

    def test_if_favorites_view_return_302_when_user_is_anonymous(self):
        response = self.client.get(reverse('FavoritesPage'))
        self.assertEquals(response.status_code, 302)

    def test_if_favorites_view_without_args_return_favorites_template(self):
        self.client.login(**self.login_data)
        response = self.client.get(reverse('FavoritesPage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites.html')

    def test_if_favorites_view_return_user_favorites(self):
        self.client.login(**self.login_data)
        self.test_user.favorites.add(self.test_product)
        response = self.client.get(reverse('FavoritesPage'))
        favorites_in_db = self.test_user.favorites.all()
        favorites_in_view = response.context['current_user_favorites_list']
        self.assertTrue(favorites_in_db[0].id == favorites_in_view[0].id)

    def test_if_favorites_view_add_product_to_user_favorites(self):
        self.client.login(**self.login_data)
        user_favorites_before = self.test_user.favorites.count()
        id = self.test_product.id
        self.client.get(reverse('AddFavorites', args=[id]))
        user_favorites_after = self.test_user.favorites.count()
        self.assertTrue(user_favorites_after > user_favorites_before)
        self.assertTrue(
            self.test_user.favorites.filter(id=self.test_product.id).exists()
        )

    def test_if_favorites_view_dont_add_product_already_in_favorites(self):
        self.client.login(**self.login_data)
        self.test_user.favorites.add(self.test_product)
        user_favorites_before = self.test_user.favorites.count()
        id = self.test_product.id
        self.client.get(reverse('AddFavorites', args=[id]))
        user_favorites_after = self.test_user.favorites.count()
        self.assertTrue(user_favorites_after == user_favorites_before)
        self.assertTrue(
            self.test_user.favorites.filter(id=self.test_product.id).exists()
        )

    def test_if_favorites_view_return_404_if_no_product_to_substitute(self):
        self.client.login(**self.login_data)
        id = FoodProduct.objects.latest('id').id + 1
        response = self.client.get(reverse('AddFavorites', args=[id]))
        self.assertEquals(response.status_code, 404)

    """ product_details view tests """

    def test_if_product_details_view_return_product_details_template(self):
        id = self.test_product.id
        response = self.client.get(reverse('productDetailsPage', args=[id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_details.html')

    def test_if_product_details_view_return_404_if_no_product_to_save(self):
        id = FoodProduct.objects.latest('id').id + 1
        response = self.client.get(reverse('productDetailsPage', args=[id]))
        self.assertEquals(response.status_code, 404)

    """ legal_disclaimers view tests """

    def test_if_legal_disclaimers_view_return_legal_disclaimers_template(self):
        response = self.client.get(reverse('LegalDisclaimersPages'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal_disclaimers.html')
