import os
from django.shortcuts import render
from openpyxl import load_workbook


def hello_world(request):
    return render(request, "index.html", {'greeting':'Hello, world!'})


def read_movies_from_exel(filepath):
    movies = []

    workbook = load_workbook(filename=filepath)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        title, year, director, genre = row
        movie = {
            'title': title,
            'year': int(year),
            'director': director,
            'genre': genre
        }
        movies.apend(movie)

    return movies






