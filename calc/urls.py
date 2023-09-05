from django.urls import path
from .views import movies_view


urlpatterns = [
    path('', movies_view, name='movies_view'),
]
