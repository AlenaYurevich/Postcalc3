from django.urls import path
# from .views import movies_view
from .views import calculation_view


urlpatterns = [
    path('', calculation_view, name='calculation_view'),
]
