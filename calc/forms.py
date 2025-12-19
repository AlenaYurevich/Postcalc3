from django import forms
from .ems_points import read_ems_points
from .sheets import sheet3, sheet5, sheet8
from .countries import read_the_country


Choices_notice = [(1, f'простое 0,84 руб.'),
                  (2, f'заказное 2,64 руб. '),
                  (3, f'электронное (посредством Viber, SMS, email) 0,54 руб.'),
                  (4, 'без уведомления',)]


class PostForm(forms.Form):
    weight = forms.IntegerField(label="Введите вес отправления, грамм", min_value=1, initial=20,
                                widget=forms.NumberInput(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", min_value=0, required=False,
                                        decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control",
                                                                                          'placeholder': "нет"}))
    notification = forms.TypedChoiceField(label="Уведомление о вручении:", choices=Choices_notice, initial=4,
                                          widget=forms.RadioSelect())


Choices = read_ems_points(sheet5)
Choices2 = [(3, 'до 10 часов рабочего дня, следующего за днем приема'),
            (2, 'в указанное время рабочего дня, следующего за днем приема'),
            (2.5, 'в день приёма'),
            (1, 'в течение рабочего дня, следующего за днем приема')]
"""
1, 3, 2, 2.5 - повышающие коэффициенты в зависимости от времени доставки
"""
International_Choices = read_the_country(sheet3)
Ems_Int_Choices = read_the_country(sheet8)


class EmsForm(forms.Form):
    departure = forms.TypedChoiceField(label="Выберите пункт отправления", choices=Choices,
                                       widget=forms.Select(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    destination = forms.TypedChoiceField(label="Выберите пункт назначения", choices=Choices,
                                         widget=forms.Select(attrs={'class': "form-control"}))
    weight = forms.IntegerField(label="Введите вес отправления, грамм", min_value=1, widget=forms.NumberInput(attrs={
        'class': "form-control"}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", min_value=0, required=False,
                                        decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control",
                                                                                          'placeholder': "нет"}))
    delivery = forms.ChoiceField(label="Доставка:", choices=Choices2,
                                 widget=forms.RadioSelect(attrs={'checked': Choices2[3]}))
    notification = forms.TypedChoiceField(label="Уведомление о вручении:", choices=Choices_notice,
                                          widget=forms.RadioSelect(attrs={'checked': Choices_notice[0]}))
    fragile = forms.BooleanField(label="С отметкой за прием хрупких и (или) громоздких", required=False,
                                 widget=forms.CheckboxInput(attrs={'class': "form-check-input border-info"}))


class TransferForm(forms.Form):
    amount = forms.DecimalField(label="Введите сумму перевода, рублей", min_value=0.01, initial=20,
                                decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control",
                                                                                  'autofocus': 'autofocus'}))


class ParcelIntForm(forms.Form):
    destination = forms.TypedChoiceField(label="Страна назначения", choices=International_Choices,
                                         widget=forms.Select(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    weight = forms.IntegerField(
        label="Введите вес отправления, грамм",
        min_value=1,
        initial=20,
        widget=forms.NumberInput(attrs={'class': "form-control", 'step': '1'}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", min_value=0, required=False,
                                        decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control",
                                                                                          'placeholder': "нет"}))


class EmsIntForm(forms.Form):
    destination = forms.TypedChoiceField(label="Страна назначения", choices=Ems_Int_Choices,
                                         widget=forms.Select(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    weight = forms.IntegerField(label="Введите вес отправления, грамм", min_value=1, widget=forms.NumberInput(attrs={
        'class': "form-control"}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", min_value=0, required=False,
                                        decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control",
                                                                                          'placeholder': "нет"}))
