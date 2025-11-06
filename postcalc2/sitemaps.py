try:
    from news.sitemaps import sitemaps as news_sitemaps
except ImportError:
    news_sitemaps = {}

try:
    from calc.sitemaps import sitemaps as calc_sitemaps
except ImportError:
    calc_sitemaps = {}

# Объединяем все sitemaps проекта
sitemaps = {}
sitemaps.update(calc_sitemaps)
sitemaps.update(news_sitemaps)
