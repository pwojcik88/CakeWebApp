from django import forms
from Tartas.models import Tartas


class CakeSearchForm(forms.Form):
    title = forms.CharField(max_length = 50, label="",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
                            required=False)

class AddCakeForm(forms.ModelForm):

    class Meta:
        model = Tartas
        fields = ['name', 'description', 'price', 'category', 'picture']

