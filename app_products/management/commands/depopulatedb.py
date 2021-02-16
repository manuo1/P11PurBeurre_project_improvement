from django.core.management.base import BaseCommand

from app_products.models import FoodCategory, FoodProduct


class Command(BaseCommand):
    def handle(self, *args, **options):
        """to erase all food products in the database."""
        FoodProduct.objects.all().delete()
        FoodCategory.objects.all().delete()
        products_in_base = FoodProduct.objects.all().count()
        categories_in_base = FoodCategory.objects.all().count()
        self.stdout.write('{} produits en base'.format(products_in_base))
        self.stdout.write('{} categorie en base'.format(categories_in_base))
