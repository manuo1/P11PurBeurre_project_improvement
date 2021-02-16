from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from app_products.models import FoodCategory, FoodProduct

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
firefox_options.add_argument('window-size=1600x900')
firefox_options.set_preference("browser.privatebrowsing.autostart", True)


class FirefoxFunctionalTestCases(LiveServerTestCase):
    """Functional tests using the Firefox web browser in headless mode."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox(options=firefox_options)
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()

    def setUp(self):

        self.test_category = FoodCategory.objects.create(
            category_name='test_category'
        )
        self.test_product = FoodProduct.objects.create(
            product_name='test product name',
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
        self.substitute = FoodProduct.objects.get(pk=self.test_product.pk)
        self.substitute.barcode += 1
        self.substitute.nutriscore = 'a'
        self.substitute.pk = None
        self.substitute.save()
        self.substitute.categories.add(self.test_category)

        self.driver.get(self.live_server_url)

    def test_index(self):
        """test simple index display."""
        self.driver.find_element_by_id('home').click()
        h1 = self.driver.find_element_by_tag_name('h1').get_attribute(
            'innerHTML'
        )
        self.assertTrue('Du gras, oui, mais de qualité !' in str(h1))

    def test_search_return_result(self):
        """test is search return a product."""
        form = self.driver.find_element_by_id('id_search')
        form.send_keys('test product name')
        form.send_keys(Keys.ENTER)
        card_footer = self.driver.find_element_by_class_name(
            'card-footer'
        ).get_attribute('innerHTML')
        self.assertTrue(self.test_product.product_name in str(card_footer))

    def test_substitute_return_substitute(self):
        """test if substitute return a substitute."""
        form = self.driver.find_element_by_id('id_search')
        form.send_keys('test product name')
        form.send_keys(Keys.ENTER)
        self.driver.find_element_by_class_name('card-footer').click()
        card_link = self.driver.find_element_by_class_name(
            'card-link'
        ).get_attribute('innerHTML')
        self.assertTrue(self.substitute.product_name in str(card_link))
