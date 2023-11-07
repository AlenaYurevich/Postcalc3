from django import forms


class PostForm(forms.Form):
    weight = forms.IntegerField(label="Введите вес отправления, грамм", widget=forms.NumberInput(attrs={
        'class': "form-control", 'autofocus': 'autofocus'}))
    declared_value = forms.DecimalField(label="Введите объявленную ценность, рублей", required=False, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': "form-control"}))
