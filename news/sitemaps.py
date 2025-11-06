from django.contrib import sitemaps
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Post, Category  # ваши модели


class NewsPaginatedSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Вычисляем количество страниц без загрузки всех постов
        total_posts = Post.objects.count()
        posts_per_page = 7
        num_pages = (total_posts + posts_per_page - 1) // posts_per_page
        return range(1, num_pages + 1)

    def location(self, page_number):
        return f"{reverse('news_index')}?page={page_number}"

    def lastmod(self, page_number):
        # Получаем только самый свежий пост для определения даты изменения
        posts_per_page = 7
        offset = (page_number - 1) * posts_per_page

        # Берем первый пост на странице (самый свежий)
        latest_post = Post.objects.order_by('-created_on')[offset:offset + 1].first()
        return latest_post.created_on if latest_post else None


class CategorySitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        # Возвращаем дату последнего поста в этой категории
        last_post = obj.posts.order_by('-last_modified').first()
        return last_post.last_modified if last_post else None

    def location(self, obj):
        return reverse('news_category', kwargs={'category_slug': obj.slug})


class NewsDynamicSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.last_modified  # используем ваше существующее поле


sitemaps = {
    # 'news_static': NewsStaticSitemap,
    'news_pages': NewsPaginatedSitemap,
    'news_categories': CategorySitemap,
    'news_posts': NewsDynamicSitemap,
}
