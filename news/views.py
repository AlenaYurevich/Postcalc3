from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def news_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
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
