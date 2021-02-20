from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, models

from app_products.models import FoodProduct


class UsersManager(models.Manager):
    """addition of a manager to the User class."""

    def get_favorites_list(self, user):
        current_user_favorites_list = user.favorites.all()
        return current_user_favorites_list

    def add_to_favorites_list(self, user, product):
        user.favorites.add(product)

    def change_username(self, user, new_username):
        message = ''
        old_username = user.username
        user.username = new_username
        try:
            user.save()
            message = "Votre nom d'utilisateur a été modifié"
        except IntegrityError:
            user.username = old_username
            message = "Ce nom d'utilisateur est déja utilisé"
        return message

    def change_first_name(self, user, new_first_name):
        message = ''
        try:
            user.first_name = new_first_name
            user.save()
            message = "Votre prénom a été modifié"
        except IntegrityError:
            pass
        return message

    def change_email(self, user, new_email):
        message = ''
        try:
            user.email = new_email
            user.save()
            message = "Votre adresse email a été modifié"
        except IntegrityError:
            pass
        return message

class User(AbstractUser):
    """addition of a relationship many to many."""

    favorites = models.ManyToManyField(FoodProduct)
