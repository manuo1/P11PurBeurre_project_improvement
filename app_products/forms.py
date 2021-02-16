from django import forms


class ProductSearchFormManager(forms.Form):
    def get_search_in(self, request_post):
        searched_product = None
        search_form = ProductSearchForm(request_post)
        if search_form.is_valid():
            searched_product = search_form.cleaned_data.get('search')
        return searched_product


class ProductSearchForm(forms.Form):
    search = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(ProductSearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'form-control'})
        self.fields['search'].widget.attrs.update({'placeholder': 'Chercher'})
