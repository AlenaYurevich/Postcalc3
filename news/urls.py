from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.news_index, name='news_index'),
    path('post/<slug:slug>/', views.news_detail, name='news_detail'),
    path('category/<slug:category_slug>/', views.news_category, name='news_category'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
