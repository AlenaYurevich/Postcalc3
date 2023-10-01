import math
import os
import requests
from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import load_workbook
from .forms import PostForm


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


weight = 69


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
    postform = PostForm()
    if request.method == "POST":
        postform = PostForm(request.POST)
        if postform.is_valid():
            weight = postform.cleaned_data("weight")
            return HttpResponse(f"<h2>Hello, {weight}</h2>")
    # cost_of_delivery = cost_of_letter(weight)
    return render(request, 'index.html', {'price_list': price_list}, {'postform': postform},)
