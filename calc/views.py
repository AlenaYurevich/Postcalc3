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



def calculation_view(request):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    price_list = read_letter_from_exel(file_path)
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    cost_of_delivery = "{:.2f}".format(sheet['B4'].value * 2)
    return render(request, 'index.html', {'price_list': price_list, 'cost_of_delivery': cost_of_delivery})




