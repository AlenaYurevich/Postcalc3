from django import forms
from .ems_points import read_ems_points, sheet


class PostForm(forms.Form):
    weight = forms.IntegerField(label="Введите вес отправления, грамм", widget=forms.NumberInput(attrs={
        'class': "form-control", 'autofocus': 'autofocus'}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", required=False, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': "нет"}))


Choices = read_ems_points(sheet)
Choices2 = [(3, 'до 10 часов рабочего дня, следующего за днем приема'),
            (2, 'в указанное время рабочего дня, следующего за днем приема'),
            (2.5, 'в день приёма'),
            (1, 'в течение рабочего дня, следующего за днем приема')]
"""
1, 3, 2, 2.5 - повышающие коэффициенты в зависимости от времени доставки
"""

Choices3 = [(1, 'простое'),
            (2, 'заказное'),
            (3, 'посредством SMS сообщения'),
            (4, 'без уведомления',)]


class EmsForm(forms.Form):
    departure = forms.TypedChoiceField(label="Выберите пункт отправления", choices=Choices,
                                       widget=forms.Select(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    destination = forms.TypedChoiceField(label="Выберите пункт назначения", choices=Choices,
                                         widget=forms.Select(attrs={'class': "form-control"}))
    weight = forms.IntegerField(label="Введите вес отправления, грамм", widget=forms.NumberInput(attrs={
        'class': "form-control"}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", required=False, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': "нет"}))
    delivery = forms.ChoiceField(label="Доставка:", choices=Choices2,
                                 widget=forms.RadioSelect(attrs={'checked': Choices2[3]}))
    notification = forms.TypedChoiceField(label="Уведомление:", choices=Choices3,
                                          widget=forms.RadioSelect(attrs={'id': "radio2", 'checked': Choices3[0]}))
    fragile = forms.BooleanField(label="За прием хрупких и (или) громоздких", required=False, widget=forms.CheckboxInput(attrs={}))
