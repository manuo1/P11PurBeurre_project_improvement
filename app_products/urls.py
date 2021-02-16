from django.urls import path

from app_products import views

urlpatterns = [
    path('', views.index, name='indexPage'),
    path('search', views.search, name='search'),
    path(
        'substitutes/<int:selected_product_id>',
        views.substitutes,
        name='substitutesPage',
    ),
    path(
        'product_details/<int:selected_product_id>',
        views.product_details,
        name='productDetailsPage',
    ),
    path('favorites/', views.favorites, name='FavoritesPage'),
    path(
        'favorites/<int:product_to_save_id>',
        views.favorites,
        name='AddFavorites',
    ),
    path(
        'legal_disclaimers/',
        views.legal_disclaimers,
        name='LegalDisclaimersPages',
    ),
]
