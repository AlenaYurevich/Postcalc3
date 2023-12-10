from django import forms


class PostForm(forms.Form):
    weight = forms.IntegerField(label="Введите вес отправления, грамм", widget=forms.NumberInput(attrs={
        'class': "form-control", 'autofocus': 'autofocus'}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", required=False, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': "нет"}))


Choices = ((1, "English"), (2, "German"), (3, "French"))


class EmsForm(forms.Form):
    departure = forms.TypedChoiceField(label="Выберите пункт отправления", choices=Choices, empty_value=2,
                                       widget=forms.Select(attrs={'class': "form-control", 'autofocus': 'autofocus'}))
    weight = forms.IntegerField(label="Введите вес отправления, грамм", widget=forms.NumberInput(attrs={
        'class': "form-control"}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", required=False, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': "нет"}))
