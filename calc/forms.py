from django import forms


class PostForm(forms.Form):
    weight = forms.IntegerField()
    declared_value = forms.FloatField()
