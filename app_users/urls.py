from django.urls import path

from app_products.forms import ProductSearchForm
from app_users import views

urlpatterns = [
    path('login', views.loginPage, name='loginPage'),
    path('register', views.registerPage, name='registerPage'),
    path('logout', views.logoutCurrentUser, name='logoutCurrentUser'),
    path('profile', views.profile, name='profilePage'),
    path('personal-information', views.userInfoPage, name='userInfoPage'),
    path(
        'update-personal-information',
        views.updateUserInfoPage,
        name='updateUserInfoPage',
    ),
    path(
        'update-password',
        views.PersonalPasswordChangeView.as_view(
            template_name='update-password.html',
            success_url='personal-information',
            extra_context={'search_form': ProductSearchForm()},
        ),
        name='update-password',
    ),
]
