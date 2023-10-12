import math
import os
# import requests
# from django.http import HttpResponseRedirect
from django.shortcuts import render
from openpyxl import load_workbook
from .forms import PostForm
from .letter import cost_of_simple


def read_letter_from_exel(filepath):
    price_list = []
    workbook = load_workbook(filename=filepath)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=3, values_only=True):
        item, cost_fiz, cost_yur = row
        rates = {
            'item': item,
            'cost_fiz': cost_fiz,
            'cost_yur': cost_yur
                    }
        price_list.append(rates)
    return price_list


def weight_step(item_weight):
    return math.ceil((item_weight - 20) / 20)


def cost_of_registered(item_weight):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    fiz = sheet['D10'].value + sheet['D18'].value * weight_step(item_weight)
    yur = (sheet['H10'].value + sheet['H18'].value * weight_step(item_weight)) * 1.2
    return [fiz, yur]


def calculation_view(request):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    price_list = read_letter_from_exel(file_path)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            item_weight = int(request.POST.get('weight'))
            declared_value = request.POST.get('declared_value')
            if declared_value:
                for_declared_value = int(declared_value) * 3 / 100
            else:
                for_declared_value = 0
            cost_of_letter_fiz = str("{:.2f}".format(cost_of_simple(item_weight)[0]).replace('.', ','))
            cost_of_letter_yur = str("{:.2f}".format(cost_of_simple(item_weight)[1]).replace('.', ','))
            cost_of_reg_fiz = str("{:.2f}".format(cost_of_registered(item_weight)[0]).replace('.', ','))
            cost_of_reg_yur = str("{:.2f}".format(cost_of_registered(item_weight)[1]).replace('.', ','))
            # cost_of_delivery = cost_of_letter_fiz + for_declared_value
            return render(request, 'index.html', {'price_list': price_list,
                                                  'form': form, 'cost_of_letter_fiz': cost_of_letter_fiz,
                                                  'cost_of_letter_yur': cost_of_letter_yur,
                                                  'cost_of_reg_fiz': cost_of_reg_fiz,
                                                  'cost_of_reg_yur': cost_of_reg_yur,
                                                  'for_declared_value': for_declared_value})  # Внутри фиг скобок
    else:
        form = PostForm()
        return render(request, 'index.html', {'price_list': price_list, 'form': form})  # внутри фигурных скобок
