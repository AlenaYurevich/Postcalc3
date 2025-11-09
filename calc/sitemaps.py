from django.contrib import sitemaps
from django.urls import reverse
from django.utils import timezone


class CalcStaticSitemap(sitemaps.Sitemap):
    # priority = 1.0
    changefreq = 'monthly'

    # def items(self):
    #     return ['main', 'ems_express_dostavka', 'internal_transfer', 'international',
    #             'ems_int', 'about']

    def items(self):
        return [
            {'name': 'main', 'priority': 1.0},
            {'name': 'ems_express_dostavka', 'priority': 0.9},
            {'name': 'internal_transfer', 'priority': 0.7},
            {'name': 'international', 'priority': 0.8},
            {'name': 'ems_int', 'priority': 0.7},
            {'name': 'about', 'priority': 0.7},

        ]

    def location(self, item):
        return reverse(item['name'])

    def priority(self, item):
        return item['priority']

    def lastmod(self, item):
        return timezone.now()


sitemaps = {
    'static': CalcStaticSitemap,
    }
