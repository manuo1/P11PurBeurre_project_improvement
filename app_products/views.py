from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app_users.models import UsersManager

from .forms import ProductSearchForm, ProductSearchFormManager
from .models import FoodProductsManager

fp_manager = FoodProductsManager()
u_manager = UsersManager()
f_manager = ProductSearchFormManager()
context = {'search_form': ProductSearchForm()}


def index(request):
    """manage the index page."""
    return render(request, 'index.html', context)


def search(request):
    """manage the search page."""
    if request.method == 'POST':
        searched_product_name = f_manager.get_search_in(request.POST)
        matching_list = fp_manager.find_matching_food_products_to(
            searched_product_name
        )
        context.update(
            {
                'searched_product': searched_product_name,
                'matching_list': matching_list,
            }
        )
    return render(request, 'search.html', context)


def substitutes(request, selected_product_id):
    """manage the substitutes page."""
    product_to_substitute = fp_manager.find_product_by_id(selected_product_id)
    substitutes_list = fp_manager.find_substitutes_to(product_to_substitute)
    context.update(
        {
            'product_to_substitute': product_to_substitute,
            'substitutes_list': substitutes_list,
        }
    )
    return render(request, 'substitutes.html', context)


def product_details(request, selected_product_id):
    """manage the product_details page."""
    product_to_display = fp_manager.find_product_by_id(selected_product_id)
    context.update({'product_to_display': product_to_display})
    return render(request, 'product_details.html', context)


@login_required()
def favorites(request, product_to_save_id=None):
    """manage the favorites (add and display) page."""
    current_user = request.user
    product_to_save = None
    current_user_favorites_list = u_manager.get_favorites_list(current_user)

    if product_to_save_id is not None:
        product_to_save = fp_manager.find_product_by_id(product_to_save_id)
        if product_to_save in current_user_favorites_list:
            messages.error(request, 'déja dans vos favorits')
        else:
            u_manager.add_to_favorites_list(current_user, product_to_save)
            messages.success(request, 'ajouté à vos favorits')
            current_user_favorites_list = u_manager.get_favorites_list(
                current_user
            )
    context.update(
        {
            'product_to_save': product_to_save,
            'current_user_favorites_list': current_user_favorites_list,
        }
    )
    return render(request, 'favorites.html', context)


def legal_disclaimers(request):
    """manage the legal_disclaimers page."""
    return render(request, 'legal_disclaimers.html', context)
