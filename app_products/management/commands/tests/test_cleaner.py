from unittest import mock

from django.test import TestCase

from ..offdata.cleaner import Cleaner
from ..offdata.constants import PRODUCT_TO_ADD_MODEL as product_model
from ..offdata.constants import USEFUL_NUTRIENTS_DATA as nutrient_fields_list
from .constants_test import (CLEANED_PRODUCT, EXPECTED_CLEANED_NUTRIENTS,
                             RAW_PRODUCT)


class CleanerUnitTest(TestCase):
    def setUp(self):
        self.path = 'app_products.management.commands.offdata.cleaner.Cleaner'

    def test_clean(self):
        """create a testing raw_products_list."""
        raw_products_list = []
        """adding 5 products products in raw_products_list"""
        while (len(raw_products_list)) < 5:
            raw_products_list.append(RAW_PRODUCT)
        with mock.patch(self.path + '.all_data_is_in', return_value=True):
            with mock.patch(
                self.path + '.nutrients',
                return_value=EXPECTED_CLEANED_NUTRIENTS,
            ):
                with mock.patch(
                    self.path + '.change_field_names',
                    return_value=CLEANED_PRODUCT['data'],
                ):
                    with mock.patch(
                        self.path + '.categories',
                        return_value=CLEANED_PRODUCT['categories'],
                    ):
                        cleaned_products_list = Cleaner.clean(
                            Cleaner, raw_products_list
                        )
                        for product in cleaned_products_list:
                            self.assertEqual(product, CLEANED_PRODUCT)

    def test_change_field_names(self):
        """test if new product fields match with model_product."""
        tested_product = Cleaner.change_field_names(Cleaner, product_model)
        for key, value in tested_product.items():
            self.assertEqual(key, value)

    def test_nutrients(self):
        """Verify that all nutrients cleaned are equivalent."""
        """to the nutrient data required."""
        expected_cleaned_nutrients = Cleaner.nutrients(Cleaner, RAW_PRODUCT)
        expected_cleaned_nutrients_list = list(
            expected_cleaned_nutrients.keys()
        )
        expected_cleaned_nutrients_list.sort()
        nutrient_fields_list.sort()
        self.assertEqual(expected_cleaned_nutrients_list, nutrient_fields_list)

    def test_categories(self):
        """check that the created category list."""
        """corresponds to the expected one"""
        returned_list = Cleaner.categories(Cleaner, RAW_PRODUCT)
        self.assertEqual(returned_list, CLEANED_PRODUCT['categories'])

    def test_all_data_is_in_return_true(self):
        """check if it return true when all are present."""
        self.assertTrue(Cleaner.all_data_is_in(Cleaner, RAW_PRODUCT))

    def test_all_data_is_in_return_false_when_1_field_missing(self):
        """check if it return false when a field is missing."""
        bad_product = RAW_PRODUCT.copy()
        del bad_product["categories"]
        self.assertFalse(Cleaner.all_data_is_in(Cleaner, bad_product))

    def test_all_data_is_in_return_false_when_1_field_is_empty(self):
        """check if it return true when a value is empty."""
        bad_product = RAW_PRODUCT.copy()
        bad_product["product_name_fr"] = ''
        self.assertFalse(Cleaner.all_data_is_in(Cleaner, bad_product))
