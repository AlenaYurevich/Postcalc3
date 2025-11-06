from django.contrib import sitemaps
from django.urls import reverse


class CalcStaticSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['main', 'ems_express_dostavka', 'internal_transfer', 'international',
                'ems_int', 'about']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': CalcStaticSitemap,
    }
