from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app_products.forms import ProductSearchForm
from .models import UsersManager

from .forms import PersonalUserCreationForm, UserInformationUpdateForm

user_manager = UsersManager()
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

@login_required()
def userInfoPage(request):
    """manage user personal information page."""
    return render(request, 'personal-information.html', context)

@login_required
def updateUserInfoPage(request):
    """manage user update personal information page."""
    if request.method == 'POST':
        user_update_form = UserInformationUpdateForm(request.POST)
        if user_update_form.is_valid():
            new_username = user_update_form.cleaned_data.get('username_update')
            new_first_name = user_update_form.cleaned_data.get('first_name_update')
            new_email = user_update_form.cleaned_data.get('email_update')
            actual_username = request.user.username
            actual_first_name = request.user.first_name
            actual_email = request.user.email
            if new_username != actual_username :
                user_manager.change_username(request.user, new_username)
            if new_first_name != actual_first_name :
                user_manager.change_first_name(request.user, new_first_name)
            if new_email != actual_email :
                user_manager.change_email(request.user, new_email)
            return render(request, 'personal-information.html', context)

    user_update_form = UserInformationUpdateForm(initial=
        {
        'username_update': request.user.username,
        'first_name_update': request.user.first_name,
        'email_update' : request.user.email,
        }
    )
    context.update({'user_update_form': user_update_form })
    return render(request, 'update-personal-information.html', context)
