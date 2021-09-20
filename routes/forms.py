from django import forms

from cities.models import City
from trains.models import Train


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(
        label='Откуда', queryset=City.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control js-example-basic-single'}
        ))

    to_city = forms.ModelChoiceField(
        label='Куда', queryset=City.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control js-example-basic-single'}
        ))
    cities = forms.ModelMultipleChoiceField(
        label='Через города',  queryset=City.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple'}
        )
    )
    travelling_time = forms.IntegerField(
        label='Вермя в пути', widget=forms.NumberInput(attrs={
             'class': 'form-control', 'placeholder': 'Введите время в пути'
        }))

    class Meta:
        model = Train
        fields = '__all__'
