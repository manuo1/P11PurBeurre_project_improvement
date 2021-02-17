from django.contrib.auth.models import AbstractUser
from django.db import models

from app_products.models import FoodProduct


class UsersManager(models.Manager):
    """addition of a manager to the User class."""

    def get_favorites_list(self, user):
        current_user_favorites_list = user.favorites.all()
        return current_user_favorites_list

    def add_to_favorites_list(self, user, product):
        user.favorites.add(product)

    def change_username(self, user, new_username):
        user.username = new_username
        user.save()

    def change_first_name(self, user, new_first_name):
        user.first_name = new_first_name
        user.save()

    def change_email(self, user, new_email):
        user.email = new_email
        user.save()

class User(AbstractUser):
    """addition of a relationship many to many."""

    favorites = models.ManyToManyField(FoodProduct)
