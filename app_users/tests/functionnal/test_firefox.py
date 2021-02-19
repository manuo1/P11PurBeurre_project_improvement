from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase, Client
from django.urls import reverse
from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
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
        self.client = Client()
        User = get_user_model()
        User.objects.create_user(
            username="testusername",
            first_name="testfirstname",
            password="testpassword",
            email="testusername@mail.com",
        )

    def test_user_can_connect_and_disconnect(self):
        """test if user can connect and disconnect."""
        self.go_to_url_name('indexPage')
        self.login_the_user ()
        self.click_on_id('button-logout')
        self.assertTrue(self.driver.find_element_by_id('button-login'))

    def test_user_can_display_his_profile(self):
        """test if user can display his profil."""
        self.go_to_url_name('indexPage')
        self.login_the_user ()
        self.click_on_id('button-profile')
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('profilePage')
        )

    def test_user_can_create_an_account(self):
        """test if user can create an account."""
        self.go_to_url_name('indexPage')
        self.click_on_id('button-login')
        self.click_on_id('button-create-account')
        self.write_in_id('id_username', "testusername2")
        self.write_in_id('id_first_name', "testuserfirstname2")
        self.write_in_id('id_email', "testusername2@mail.com")
        self.write_in_id('id_password1', "testpassword2")
        self.write_in_id('id_password2', "testpassword2")
        self.click_on_id('button-create-submit')
        self.assertTrue(
            "Un nouveau compte vient d'être créé pour testusername2"
            in
            self.get_html_in('login-messages')
        )

    def test_user_can_update_his_personnal_info(self):
        """test if user can update his personnals informations."""
        self.login_the_user ()
        self.go_to_url_name('updateUserInfoPage')
        self.write_in_id('id_username_update', 'testusername3')
        self.write_in_id('id_first_name_update', 'testfirstname3')
        self.write_in_id('id_email_update', 'testusername3@mail.com')
        self.click_on_id('button-user-info-update-submit')
        confirmation_messages = self.get_html_in('messages')
        self.assertTrue(
            "Votre nom d'utilisateur a été modifié" in confirmation_messages
            and
            "Votre prénom a été modifié" in confirmation_messages
            and
            "Votre adresse email a été modifié" in confirmation_messages
        )

    def test_user_can_update_his_password(self):
        """test if user can update his personnals informations."""
        self.login_the_user ()
        self.go_to_url_name('update-password')
        self.write_in_id('id_old_password', 'testpassword')
        self.write_in_id('id_new_password1', 'New_testpassword')
        self.write_in_id('id_new_password2', 'New_testpassword')
        self.click_on_id('button-psw-update-submit')
        self.go_to_url_name('logoutCurrentUser')
        self.login_the_user (password='New_testpassword')
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('profilePage')
        )

    def login_the_user(self, username='testusername', password='testpassword'):
        """test if user can connect and disconnect."""
        self.go_to_url_name('indexPage')
        self.click_on_id('button-login')
        self.write_in_id('id_username', username)
        self.write_in_id('id_password', password)
        self.click_on_id('button-login-submit')

    def write_in_id(self, element_id, value):
        element = self.driver.find_element_by_id(element_id)
        element.clear()
        element.send_keys(value)

    def click_on_id(self, element_id):
        self.driver.find_element_by_id(element_id).click()

    def get_html_in(self, element_id):
        html = self.driver.find_element_by_id(element_id
            ).get_attribute('innerHTML')
        return html

    def go_to_url_name(self, url_name):
        self.driver.get(self.live_server_url + reverse(url_name))
