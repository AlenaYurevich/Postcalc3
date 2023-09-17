from django.urls import path
from .views import movies_view
# from .views import calculation_view


urlpatterns = [
    path('', movies_view, name='movies_view'),
]
