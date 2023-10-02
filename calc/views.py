import math
import os
# import requests
from django.shortcuts import render
# from django.http import HttpResponse
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


# weight1 = 69


def cost_of_letter(item_weight):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    weight_step = math.ceil((item_weight - 20) / 20)
    cost_of_delivery = str("{:.2f}".format(sheet['B4'].value + sheet['B5'].value * weight_step)).replace('.', ',')
    return cost_of_delivery


def calculation_view(request):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    price_list = read_letter_from_exel(file_path)
    if request.method == 'POST':
        mass = float(request.POST.get('mass'))
        cost_of_delivery = cost_of_letter(mass)
        return render(request, 'index.html', {'price_list': price_list, 'cost_of_delivery': cost_of_delivery,
                                              })  # внутри фигурных скобок
    else:
        return render(request, 'index.html', {'price_list': price_list})  # внутри фигурных скобок
