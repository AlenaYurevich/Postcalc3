from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.core.paginator import Paginator


def news_index(request):
    posts = Post.objects.all().order_by('-created_on')
    paginator = Paginator(posts, 7)  # Show 7 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, 'news_index.html', context)


def news_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        "post": post
    }
    return render(request, 'news_detail.html', context)


def news_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    posts = Post.objects.filter(
        categories__slug__contains=category_slug
    ).order_by(
        '-created_on')
    context = {
        'category': category,
        'posts': posts  # здесь выводим посты Posts
    }
    return render(request, 'news_category.html', context)
