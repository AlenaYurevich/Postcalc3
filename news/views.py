from django.http import HttpResponse


def index(request):
    return HttpResponse(request, "Страница приложения news")


def categories(request):
    return HttpResponse(request, "<h1>Статьи по категориям</h1>")
