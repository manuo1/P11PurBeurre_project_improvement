from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError

from app_products.models import FoodProduct


class UsersManager(models.Manager):
    """addition of a manager to the User class."""

    def get_favorites_list(self, user):
        current_user_favorites_list = user.favorites.all()
        return current_user_favorites_list

    def add_to_favorites_list(self, user, product):
        user.favorites.add(product)

    def change_username(self, user, new_username):
        try:
            user.username = new_username
            user.save()
            return "Votre nom d'utilisateur a été modifié"
        except IntegrityError:
            return "Ce nom d'utilisateur est déja utilisé"

    def change_first_name(self, user, new_first_name):
        try:
            user.first_name = new_first_name
            user.save()
            return "Votre prénom a été modifié"
        except IntegrityError:
            pass

    def change_email(self, user, new_email):
        try:
            user.email = new_email
            user.save()
            return "Votre adresse email a été modifié"
        except IntegrityError:
            pass

class User(AbstractUser):
    """addition of a relationship many to many."""

    favorites = models.ManyToManyField(FoodProduct)
