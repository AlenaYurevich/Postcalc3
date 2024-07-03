from django import forms
from .ems_points import read_ems_points, sheet
from .ems_cost import notification_list
from .format import formatted


N = [formatted(i * 1.2) for i in notification_list]

Choices_notice = [(1, f'простое {N[0]} руб.'),
                  (2, f'заказное {N[1]} руб. '),
                  (3, f'электронное (посредством Viber, SMS, email) {N[2]} руб.'),
                  (4, 'без уведомления',)]


class PostForm(forms.Form):
    weight = forms.IntegerField(label="Введите вес отправления, грамм", min_value=0, widget=forms.NumberInput(attrs={
        'class': "form-control", 'autofocus': 'autofocus'}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", min_value=0, required=False,
                                        decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control",
                                                                                          'placeholder': "нет"}))
    notification = forms.TypedChoiceField(label="Уведомление:", choices=Choices_notice,
                                          widget=forms.RadioSelect(attrs={'checked': Choices_notice[0]}))


Choices = read_ems_points(sheet)
Choices2 = [(3, 'до 10 часов рабочего дня, следующего за днем приема'),
            (2, 'в указанное время рабочего дня, следующего за днем приема'),
            (2.5, 'в день приёма'),
            (1, 'в течение рабочего дня, следующего за днем приема')]
"""
1, 3, 2, 2.5 - повышающие коэффициенты в зависимости от времени доставки
"""


class EmsForm(forms.Form):
    departure = forms.TypedChoiceField(label="Выберите пункт отправления", choices=Choices,
                                       widget=forms.Select(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    destination = forms.TypedChoiceField(label="Выберите пункт назначения", choices=Choices,
                                         widget=forms.Select(attrs={'class': "form-control"}))
    weight = forms.IntegerField(label="Введите вес отправления, грамм", min_value=0, widget=forms.NumberInput(attrs={
        'class': "form-control"}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", min_value=0, required=False,
                                        decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control",
                                                                                          'placeholder': "нет"}))
    delivery = forms.ChoiceField(label="Доставка:", choices=Choices2,
                                 widget=forms.RadioSelect(attrs={'checked': Choices2[3]}))
    notification = forms.TypedChoiceField(label="Уведомление:", choices=Choices_notice,
                                          widget=forms.RadioSelect(attrs={'checked': Choices_notice[0]}))
    fragile = forms.BooleanField(label="С отметкой за прием хрупких и (или) громоздких", required=False,
                                 widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
