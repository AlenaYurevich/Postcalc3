from django import forms
from .ems_points import read_ems_points, sheet


class PostForm(forms.Form):
    weight = forms.IntegerField(label="Введите вес отправления, грамм", widget=forms.NumberInput(attrs={
        'class': "form-control", 'autofocus': 'autofocus'}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", required=False, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': "нет"}))


Choices = read_ems_points(sheet)
Choices2 = [('1', 'в течение рабочего дня, следующего за днем приема'),
            ('2', 'до 10 часов рабочего дня, следующего за днем приема'),
            ('3', 'в указанное время рабочего дня, следующего за днем приема')]


class EmsForm(forms.Form):
    departure = forms.TypedChoiceField(label="Выберите пункт отправления", choices=Choices,
                                       widget=forms.Select(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    destination = forms.TypedChoiceField(label="Выберите пункт назначения", choices=Choices,
                                         widget=forms.Select(attrs={'class': "form-control"}))
    weight = forms.IntegerField(label="Введите вес отправления, грамм", widget=forms.NumberInput(attrs={
        'class': "form-control"}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", required=False, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': "нет"}))
    delivery = forms.ChoiceField(label="Доставка:", choices=Choices2, widget=forms.RadioSelect(attrs={'class': "col"}))
