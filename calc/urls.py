from django.urls import path
from django.views.generic import TemplateView
from .views import calculation_view
from .views import ems_view, about_view, internal_transfer_view
from .views import international_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', calculation_view, name='main'),
    path('main', calculation_view, name='main'),
    path('ems_express_dostavka', ems_view, name='ems_express_dostavka'),
    path('internal_transfer', internal_transfer_view, name='internal_transfer'),
    path('international', international_view, name='international'),
    path('about', about_view, name='about'),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
