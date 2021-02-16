from .constants import ESSENTIAL_PRODUCT_DATA as product_fields_list
from .constants import \
    MAXIMUM_QUANTITY_OF_CATEGORIES_TO_KEEP_PER_PRODUCT as max_of_categories
from .constants import PRODUCT_TO_ADD_MODEL as product_model
from .constants import USEFUL_NUTRIENTS_DATA as nutrient_fields_list


class Cleaner:
    def __init__(self):
        pass

    def clean(self, raw_products_list):
        """return a list of cleaned products."""
        cleaned_products_list = []
        for raw_product in raw_products_list:
            cleaned_product = {'data': {}, 'categories': []}
            all_data_is_in_the_raw_product = self.all_data_is_in(raw_product)
            if all_data_is_in_the_raw_product:
                """adds first data of product_fields_list."""
                for field in product_fields_list[:4]:
                    cleaned_product['data'][field] = raw_product[field]
                """adds nutrients"""
                product_nutrients = self.nutrients(raw_product)
                cleaned_product['data'] = {
                    **cleaned_product['data'],
                    **product_nutrients,
                }
                """changes fields names"""
                cleaned_product['data'] = self.change_field_names(
                    cleaned_product['data']
                )
                """adds categories"""
                cleaned_product['categories'] = self.categories(raw_product)
                """add cleaned product to the list"""
                cleaned_products_list.append(cleaned_product)
        return cleaned_products_list

    def change_field_names(self, product):
        """replaces the field names for those in the FoodProduct table."""
        for field in product_model.keys():
            if field in product.keys():
                old_field = field
                new_field = product_model[field]
                product[new_field] = product.pop(old_field)
        return product

    def nutrients(self, product):
        """return a dictionary of useful nutrient fields in the product."""
        raw_nutrients = product['nutriments']
        cleaned_nutrients = {}
        for field in nutrient_fields_list:
            if field in raw_nutrients.keys():
                if isinstance(raw_nutrients[field], (int, float)):
                    cleaned_nutrients[field] = round(raw_nutrients[field], 2)
                else:
                    cleaned_nutrients[field] = raw_nutrients[field]
            else:
                cleaned_nutrients[field] = ''
        return cleaned_nutrients

    def categories(self, product):
        """return a list of the product categories."""
        raw_categories = product['categories'].split(',')
        cleaned_categories = []
        for category in raw_categories:
            if len(cleaned_categories) < max_of_categories:
                if category[0] == ' ':
                    cleaned_categories.append(category[1:])
                else:
                    cleaned_categories.append(category)

        return cleaned_categories

    def all_data_is_in(self, product):
        """check if the product contains all the essential data."""
        if all(
            field in product.keys() for field in product_fields_list
        ) and all(product[field] != '' for field in product_fields_list):
            product_contains_all_data = True
        else:
            product_contains_all_data = False
        return product_contains_all_data
