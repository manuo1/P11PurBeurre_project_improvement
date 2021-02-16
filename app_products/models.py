from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404


class FoodProductsManager(models.Manager):
    def find_product_by_id(self, id):
        """return the object corresponding to the requested id."""
        product = get_object_or_404(FoodProduct, id=id)
        return product

    def find_matching_food_products_to(self, searched_product_name):
        """returns a list of objects corresponding to the searched words."""
        matching_list = []
        matching_list = (
            FoodProduct.objects.annotate(search=SearchVector('product_name'))
            .filter(search=SearchQuery(searched_product_name))
            .order_by('product_name')
        )
        if len(matching_list) > 9:
            matching_list = matching_list[:9]
        return matching_list

    def find_substitutes_to(self, product_to_substitute):
        """Returns a list of food products that have the greatest number of
        categories in common with the product to be substituted and a lower
        nutrient score."""
        substitutes_list = []
        product_to_substitute_categories = (
            product_to_substitute.categories.all()
        )
        product_to_substitute_nutriscore = product_to_substitute.nutriscore

        """
        annotate :  annotate products with sum of common categories with
                    the product to be substituted
        filter: categories identical to those of the product to be substituted
                and nutriscor lower than that of the product to be substituted
        order : decreasing number of categories in common
                and increasing nutriscore value
        """
        substitutes_list = (
            FoodProduct.objects.annotate(common_categories=Count('categories'))
            .filter(
                categories__in=product_to_substitute_categories,
                nutriscore__lt=product_to_substitute_nutriscore,
            )
            .order_by('-common_categories', 'nutriscore')
        )
        if len(substitutes_list) > 8:
            substitutes_list = substitutes_list[:9]
        return substitutes_list


class FoodCategory(models.Model):
    """stock all categories."""

    category_name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.category_name


class FoodProduct(models.Model):
    """stock food product data."""

    product_name = models.CharField(max_length=300)
    nutriscore = models.CharField(max_length=1)
    barcode = models.PositiveBigIntegerField(unique=True)
    image_url = models.URLField(max_length=300)
    energy_kj = models.CharField(max_length=20)
    energy_kcal = models.CharField(max_length=20)
    protein = models.CharField(max_length=20)
    glucid = models.CharField(max_length=20)
    lipid = models.CharField(max_length=20)
    fiber = models.CharField(max_length=20)
    salt = models.CharField(max_length=20)
    """ associates food products with their categories """
    categories = models.ManyToManyField(FoodCategory)

    def __str__(self):
        return self.product_name
