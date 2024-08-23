from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_index, name='news_index'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('<category>/', views.news_category, name='news_category'),
]
