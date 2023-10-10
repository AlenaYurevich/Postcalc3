from django import forms


class PostForm(forms.Form):
    weight = forms.IntegerField(label="Введите вес отправления, грамм")
    declared_value = forms.FloatField(label="Введите объявленную ценность, рублей")

