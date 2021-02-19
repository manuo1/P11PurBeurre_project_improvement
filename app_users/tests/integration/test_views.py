from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAppUsersViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.test_user_1 = self.User.objects.create_user(
            username='test_name',
            email='test_mail@mail.com',
            password='test_password',
            first_name='test_first_name',
        )
        self.reg_form = {
            'username': 'test_name_2',
            'first_name': 'test_first_name_2',
            'email': 'test_mail_2@mail.com',
            'password1': 'test_password_2',
            'password2': 'test_password_2',
        }
        self.log_form = {'username': 'test_name', 'password': 'test_password'}

    def test_login_succes(self):
        response = self.client.post(reverse('loginPage'), self.log_form)
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)
        self.assertRedirects(response, '/user/profile')

    def test_login_fail(self):
        self.log_form['password'] = 'wrong_password'
        response = self.client.post(reverse('loginPage'), self.log_form)
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, False)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_when_user_is_already_authenticated(self):
        self.client.login(**self.log_form)
        response = self.client.get(reverse('loginPage'))
        self.assertRedirects(response, '/')

    def test_login_with_next_url_redirect(self):
        response = self.client.get(reverse('FavoritesPage'))
        self.assertRedirects(response, '/user/login?next=/favorites/')
        response = self.client.post(
            '/user/login?next=/favorites/', self.log_form
        )
        self.assertRedirects(response, '/favorites/')

    def test_registration_succes(self):
        response = self.client.post(reverse('registerPage'), self.reg_form)
        self.assertEquals(
            self.User.objects.filter(
                username=self.reg_form['username']
            ).exists(),
            True,
        )
        self.assertRedirects(response, '/user/login')

    def test_registration_failure(self):
        self.reg_form['password2'] = 'wrong_password_2'
        response = self.client.post(reverse('registerPage'), self.reg_form)
        self.assertEquals(
            self.User.objects.filter(
                username=self.reg_form['username']
            ).exists(),
            False,
        )
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_when_user_is_authenticated(self):
        self.client.login(**self.log_form)
        response = self.client.post(reverse('registerPage'), self.reg_form)
        self.assertRedirects(response, '/')

    def test_logout_view_when_user_is_authenticated(self):
        self.client.login(**self.log_form)
        response = self.client.get(reverse('logoutCurrentUser'))
        user = auth.get_user(self.client)
        self.assertEquals(user.is_anonymous, True)
        self.assertRedirects(response, '/')

    def test_logout_view_when_user_is_anonymous(self):
        response = self.client.get(reverse('logoutCurrentUser'))
        self.assertRedirects(response, '/user/login?next=/user/logout')

    def test_profile_view_when_user_is_authenticated(self):
        self.client.login(**self.log_form)
        response = self.client.get(reverse('profilePage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_when_user_is_anonymous(self):
        response = self.client.get(reverse('profilePage'))
        self.assertRedirects(response, '/user/login?next=/user/profile')

    def test_if_user_can_change_their_personnal_info(self):
        self.client.login(**self.log_form)
        new_data_form = {
            'username_update': 'test_name_3',
            'first_name_update': 'test_first_name_3',
            'email_update': 'test_mail_3@mail.com',
        }
        response = self.client.post(
            reverse('updateUserInfoPage'), new_data_form
        )
        modified_user = auth.get_user(self.client)
        self.assertTrue(
            modified_user.username == new_data_form['username_update']
            and
            modified_user.first_name == new_data_form['first_name_update']
            and
            modified_user.email == new_data_form['email_update']
        )

    def test_if_user_can_change_his_password(self):
        """ login with curent password """
        self.client.login(**self.log_form)
        new_password_form = {
            'old_password': 'test_password',
            'new_password1': 'new_test_password',
            'new_password2': 'new_test_password',
        }
        """ change password """
        self.client.post(
            reverse('update-password'), new_password_form
        )
        """ logout """
        self.client.get(reverse('logoutCurrentUser'))
        """ login with new password """
        self.log_form['password']='new_test_password'
        response = self.client.post(reverse('loginPage'), self.log_form)
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)
        self.assertRedirects(response, '/user/profile')
