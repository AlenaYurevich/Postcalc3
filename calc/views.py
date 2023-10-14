import math
import os
# import requests
# from django.http import HttpResponseRedirect
from django.shortcuts import render
from openpyxl import load_workbook
from .forms import PostForm
from .letter import cost_of_simple
from .letter import cost_of_registered


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


def formatted(num):
    return str("{:.2f}".format(num).replace('.', ','))


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
            cost_of_letter_fiz = formatted(cost_of_simple(item_weight)[0])
            cost_of_letter_yur = formatted(cost_of_simple(item_weight)[1])
            vat_simple = formatted(cost_of_simple(item_weight)[2])
            cost_of_reg_fiz = formatted(cost_of_registered(item_weight)[0])
            cost_of_reg_yur = formatted(cost_of_registered(item_weight)[1])
            vat_registered = formatted(cost_of_registered(item_weight)[2])
            # cost_of_delivery = cost_of_letter_fiz + for_declared_value
            return render(request, 'index.html', {'price_list': price_list,
                                                  'form': form, 'cost_of_letter_fiz': cost_of_letter_fiz,
                                                  'cost_of_letter_yur': cost_of_letter_yur,
                                                  'vat_simple': vat_simple,
                                                  'cost_of_reg_fiz': cost_of_reg_fiz,
                                                  'cost_of_reg_yur': cost_of_reg_yur,
                                                  'vat_registered': vat_registered,
                                                  'for_declared_value': for_declared_value})  # Внутри фиг скобок
    else:
        form = PostForm()
        return render(request, 'index.html', {'price_list': price_list, 'form': form})  # внутри фигурных скобок
