from django.test import SimpleTestCase
from django.urls import resolve, reverse

from app_products.views import (favorites, index, legal_disclaimers,
                                product_details, search, substitutes)


class TestAppProductsUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('indexPage')
        self.assertEquals(resolve(url).func, index)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_substitutespage_url_resolves(self):
        url = reverse('substitutesPage', args=[0])
        self.assertEquals(resolve(url).func, substitutes)

    def test_productdetailspage_url_resolves(self):
        url = reverse('productDetailsPage', args=[0])
        self.assertEquals(resolve(url).func, product_details)

    def test_favorites_display_url_resolves(self):
        url = reverse('FavoritesPage')
        self.assertEquals(resolve(url).func, favorites)

    def test_favorite_add_url_resolves(self):
        url = reverse('AddFavorites', args=[0])
        self.assertEquals(resolve(url).func, favorites)

    def test_legal_disclaimers_url_resolves(self):
        url = reverse('LegalDisclaimersPages')
        self.assertEquals(resolve(url).func, legal_disclaimers)
