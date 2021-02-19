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
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('button-login').click()
        self.driver.find_element_by_id('id_username').send_keys("testusername")
        self.driver.find_element_by_id('id_password').send_keys("testpassword")
        self.driver.find_element_by_id('button-login-submit').click()
        self.driver.find_element_by_id('button-logout').click()
        self.assertTrue(self.driver.find_element_by_id('button-login'))

    def test_user_can_display_his_profile(self):
        """test if user can display his profil."""
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

    def test_user_can_update_his_personnal_info(self):
        """test if user can update his personnals informations."""
        self.user_login()
        self.driver.get(self.live_server_url + reverse('updateUserInfoPage'))
        """find form fields"""
        username_field = self.driver.find_element_by_id(
            'id_username_update')
        first_name_field = self.driver.find_element_by_id(
            'id_first_name_update')
        email_field = self.driver.find_element_by_id(
            'id_email_update')
        """clear form fields """
        username_field.clear()
        first_name_field.clear()
        email_field.clear()
        """ fill form fields """
        username_field.send_keys("testusername3")
        first_name_field.send_keys("testfirstname3")
        email_field.send_keys("testusername3@mail.com")
        self.driver.find_element_by_id(
            'button-user-info-update-submit').click()
        messages = self.driver.find_element_by_id('messages'
            ).get_attribute('innerHTML')
        self.assertTrue(
            "Votre nom d'utilisateur a été modifié" in messages
            and
            "Votre prénom a été modifié" in messages
            and
            "Votre adresse email a été modifié" in messages)

    def test_user_can_update_his_password(self):
        """test if user can update his personnals informations."""
        self.user_login()
        self.driver.get(self.live_server_url + reverse('update-password'))
        self.driver.find_element_by_id('id_old_password').send_keys(
            'testpassword'
        )
        self.driver.find_element_by_id('id_new_password1').send_keys(
            'New_testpassword'
        )
        self.driver.find_element_by_id('id_new_password2').send_keys(
            'New_testpassword'
        )
        self.driver.find_element_by_id('button-psw-update-submit').click()
        self.driver.get(self.live_server_url + reverse('logoutCurrentUser'))
        self.user_login(password='New_testpassword')
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('profilePage')
        )

    def user_login(self, username='testusername', password='testpassword'):
        """test if user can connect and disconnect."""
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('button-login').click()
        self.driver.find_element_by_id('id_username').send_keys(username)
        self.driver.find_element_by_id('id_password').send_keys(password)
        self.driver.find_element_by_id('button-login-submit').click()
