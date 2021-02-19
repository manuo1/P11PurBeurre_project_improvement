from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class PersonalUserCreationForm(UserCreationForm):
    """addition of additional fields to the basic user profile."""

    """ and the form-control class for bootstrap"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Votre nom d\'utilisateur'}
            ),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Votre Prénom'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Votre adresse email'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PersonalUserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserInformationUpdateForm(forms.Form):
    username_update = forms.CharField(initial="Nom", max_length=100)
    first_name_update = forms.CharField(initial="Prénom", max_length=100)
    email_update = forms.EmailField(initial="Email", max_length=100)

    def __init__(self, *args, **kwargs):
        super(UserInformationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username_update'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['first_name_update'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['email_update'].widget.attrs.update(
            {'class': 'form-control'}
        )
