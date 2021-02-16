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


class User(AbstractUser):
    """addition of a relationship many to many."""

    favorites = models.ManyToManyField(FoodProduct)
