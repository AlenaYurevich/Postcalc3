from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import calculation_view
from .views import ems_view, page_not_found_view, about_view
from django.conf.urls import handler404


urlpatterns = [
    path('', calculation_view, name='main'),
    path('main', calculation_view, name='main'),
    path('ems_express_dostavka', ems_view, name='ems_express_dostavka'),
    path('about', about_view, name='about'),
    re_path(r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]


# handler404 = 'page_not_found_view'
