from django.shortcuts import render
from letter import letter


def hello_world(request):
    return render(request, "index.html", {'greeting': 'Hello, world!'})


# def read_movies_from_exel(filepath):
#     movies = []
#
#     workbook = load_workbook(filename=filepath)
#     sheet = workbook.active
#
#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         title, year, director, genre = row
#         movie = {
#             'title': title,
#             'year': int(year),
#             'director': director,
#             'genre': genre
#         }
#         movies.append(movie)
#
#     return movies
#
#
# def movies_view(request):
#     file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/movies.xlsx')
#     movies = read_movies_from_exel(file_path)
#     return render(request, 'index.html', {'movies': movies})


parcel_weight = int(input("Введите вес грамм"))
print(letter(parcel_weight))
