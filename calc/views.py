# import math
import os
from django.shortcuts import render
from openpyxl import load_workbook


def read_letter_from_exel(filepath):
    price_list = []

    workbook = load_workbook(filename=filepath)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=3, values_only=True):
        item, cost = row
        rates = {
            'item': item,
            'cost': cost
                    }
        price_list.append(rates)

    return price_list


def movies_view(request):
    file_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    price_list = read_letter_from_exel(file_path2)
    return render(request, 'index.html', {'price_list': price_list})




