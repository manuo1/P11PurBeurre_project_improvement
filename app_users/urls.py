from django.urls import path

from app_users import views

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('logout/', views.logoutCurrentUser, name='logoutCurrentUser'),
    path('profile/', views.profile, name='profilePage'),
]
