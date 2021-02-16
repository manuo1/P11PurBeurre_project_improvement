from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app_products.forms import ProductSearchForm

from .forms import PersonalUserCreationForm

context = {'search_form': ProductSearchForm()}


def registerPage(request):
    """manage user account creation page."""
    if request.user.is_authenticated:
        return redirect('indexPage')
    form = PersonalUserCreationForm()
    if request.method == 'POST':
        form = PersonalUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(
                request, 'Un nouveau compte vient d\'être créé pour ' + user
            )
            return redirect('loginPage')
    context.update({'form': form})
    return render(request, 'register.html', context)


def loginPage(request):
    """manage user authentication page."""
    if request.user.is_authenticated:
        return redirect('indexPage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url != '/':
                return redirect(next_url)
            return redirect('profilePage')
        else:
            messages.error(
                request, 'Nom d\'utilisateur OU mot de passe incorrect'
            )
    return render(request, 'login.html', context)


@login_required()
def logoutCurrentUser(request):
    """manage user logout page."""
    logout(request)
    return redirect('indexPage')


@login_required()
def profile(request):
    """manage user profile page."""
    return render(request, 'profile.html', context)
