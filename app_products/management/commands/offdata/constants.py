API_OFF_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"

API_OFF_PARAMS = {
    'action': 'process',
    'sort_by': 'unique_scans_n',
    'json': 'true',
    'page': 1,
    'page_size': 1000,
}
MAXIMUM_QUANTITY_OF_CATEGORIES_TO_KEEP_PER_PRODUCT = 20
ESSENTIAL_PRODUCT_DATA = [
    'product_name_fr',
    'nutrition_grade_fr',
    'code',
    'image_url',
    'categories',
    'nutriments',
]
USEFUL_NUTRIENTS_DATA = [
    'energy-kj_100g',
    'energy-kcal_100g',
    'proteins_100g',
    'carbohydrates_100g',
    'fat_100g',
    'fiber_100g',
    'salt_100g',
]
PRODUCT_TO_ADD_MODEL = {
    'product_name_fr': 'product_name',
    'nutrition_grade_fr': 'nutriscore',
    'code': 'barcode',
    'image_url': 'image_url',
    'energy-kj_100g': 'energy_kj',
    'energy-kcal_100g': 'energy_kcal',
    'proteins_100g': 'protein',
    'carbohydrates_100g': 'glucid',
    'fat_100g': 'lipid',
    'fiber_100g': 'fiber',
    'salt_100g': 'salt',
}
