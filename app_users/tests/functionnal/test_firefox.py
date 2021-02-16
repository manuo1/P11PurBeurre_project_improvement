from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver

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
        User = get_user_model()
        User.objects.create_user(
            username="testusername",
            password="testpassword",
            email="testusername@mail.com",
        )

    def test_user_can_connect_and_disconnect(self):
        """test if user can connect and disconnect."""
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('button-login').click()
        self.driver.find_element_by_id('id_username').send_keys("testusername")
        self.driver.find_element_by_id('id_password').send_keys("testpassword")
        self.driver.find_element_by_id('button-login-submit').click()
        self.driver.find_element_by_id('button-logout').click()
        self.assertTrue(self.driver.find_element_by_id('button-login'))

    def test_user_can_display_his_profile(self):
        """test if user can display is profil."""
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('button-login').click()
        self.driver.find_element_by_id('id_username').send_keys("testusername")
        self.driver.find_element_by_id('id_password').send_keys("testpassword")
        self.driver.find_element_by_id('button-login-submit').click()
        self.driver.find_element_by_id('button-profile').click()
        email = self.driver.find_element_by_id('profile-mail').get_attribute(
            'innerHTML'
        )
        self.assertEqual(email, " testusername@mail.com ")

    def test_user_can_create_an_account(self):
        """test if user can create an account."""
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('button-login').click()
        self.driver.find_element_by_id('button-create-account').click()
        self.driver.find_element_by_id('id_username').send_keys(
            "testusername2"
        )
        self.driver.find_element_by_id('id_first_name').send_keys(
            "testuserfirstname2"
        )
        self.driver.find_element_by_id('id_email').send_keys(
            "testusername2@mail.com"
        )
        self.driver.find_element_by_id('id_password1').send_keys(
            "testpassword2"
        )
        self.driver.find_element_by_id('id_password2').send_keys(
            "testpassword2"
        )
        self.driver.find_element_by_id('button-create-submit').click()
        message = self.driver.find_element_by_id(
            'login-messages'
        ).get_attribute('innerHTML')
        self.assertEqual(
            message, " Un nouveau compte vient d'être créé pour testusername2 "
        )
