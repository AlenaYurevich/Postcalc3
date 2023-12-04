from django.urls import path
# from .views import movies_view
from .views import calculation_view
from .views import ems_view


urlpatterns = [
    path('', calculation_view, name='calculation_view'),
    path('ems_express_dostavka', ems_view, name='ems_view'),
]
