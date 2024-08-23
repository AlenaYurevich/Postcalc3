from django.shortcuts import render
from .models import Post


def news_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, 'news_index.html', context)


def news_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post": post
    }
    return render(request, 'news_detail.html', context)


def news_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on')
    context = {
        'category': category,
        'posts': posts  # здесь выводим посты Posts
    }
    return render(request, 'news_category.html', context)
