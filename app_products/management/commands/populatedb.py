import os


from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from app_products.models import FoodCategory, FoodProduct
from .offdata.cleaner import Cleaner
from .offdata.download import Download

class Command(BaseCommand):
    help = """Populate database with food products from the Open Food Fact API,
            Requires a quantity of food products to be added,
            Example to add 10 products: \"python manage.py populatedb 10\" """

    def add_arguments(self, populatedb):
        """allows the user to set the number of food products."""
        """ to be loaded into the database."""
        populatedb.add_argument('quantity', type=int)

    def handle(self, *args, **options):
        """main controler."""
        food_data = self.get_food_products_data(options['quantity'])
        self.add_food_products_in_database(food_data)

    def get_food_products_data(self, quantity):
        """get food products from open food fact."""
        download = Download()
        cleaner = Cleaner()
        data_to_add = []
        page_number = 1
        self.stdout.write('\nDonnées alimentaires avant la mise à jour :')
        self.stdout.write(self.db_infos())
        self.stdout.write('\nTéléchargement des aliments...')
        while len(data_to_add) < quantity:
            raw_products_list = download.raw_data(page_number)
            cleaned_products_list = cleaner.clean(raw_products_list)
            data_to_add.extend(cleaned_products_list)
            if len(data_to_add) >= quantity:
                data_to_add = data_to_add[:quantity]
                break
            page_number += 1
        self.stdout.write('\n{} aliments téléchargés'.format(len(data_to_add)))
        return data_to_add

    def db_infos(self):
        products_qty = FoodProduct.objects.all().count()
        categories_qty = FoodCategory.objects.all().count()
        joins_qty = FoodProduct.objects.filter(categories__gte=1).count()
        total_rows_for_food_data = products_qty + categories_qty + joins_qty
        db_infos = (
            '\n     {} lignes en base pour les données alimentaires\n'
            '     ({} aliments, {} categories, {} jointures)'.format(
                total_rows_for_food_data,
                products_qty,
                categories_qty,
                joins_qty,
            )
        )
        return db_infos

    def add_infos_to_populatedb_log(self, msg):
        populatedb_log_file = os.path.join(settings.BASE_DIR, 'populatedb.log')
        with open(populatedb_log_file, "a") as log:
            log.write("\n" + str(datetime.now()) + "\n" + msg)
            log.write(str(self.db_infos()))


    def add_food_products_in_database(self, data_to_add):
        """add cleaned and formated food products in data base."""
        self.stdout.write('\nAjout des données dans la base...')
        for product in data_to_add:
            """add product to the FoodProduct table."""
            product_to_add = FoodProduct(**product['data'])
            try:
                product_to_add.save()
            except IntegrityError:
                pass
            """adds the product categories in the FoodCategory table"""
            for category in product['categories']:
                category_to_add = FoodCategory(category_name=category)
                try:
                    category_to_add.save()
                except IntegrityError:
                    pass
                """ associates the product to its categories """
                """ first gets objects in the tables to get ids """
                category_to_associate = FoodCategory.objects.get(
                    category_name=category
                )
                product_to_associate = FoodProduct.objects.get(
                    barcode=product['data']['barcode']
                )
                """ then builds the association"""
                product_to_associate.categories.add(category_to_associate)
        self.stdout.write('\nDonnées alimentaires après la mise à jour :')
        self.stdout.write(self.db_infos())
        self.add_infos_to_populatedb_log('--> populatedb terminé')
