import math
# import requests
# from django.http import HttpResponseRedirect
from django.shortcuts import render
from openpyxl import load_workbook
from .forms import PostForm
from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter, cost_for_declared_value


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
    # file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    # price_list = read_letter_from_exel(file_path)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            item_weight = int(request.POST.get('weight'))
            declared_value = request.POST.get('declared_value')
            if declared_value:
                cost_of_value_fiz = formatted(cost_of_value_letter(item_weight, declared_value)[0])
                cost_of_value_yur = formatted(cost_of_value_letter(item_weight, declared_value)[1])
                vat_value_letter = formatted(cost_of_value_letter(item_weight, declared_value)[2])
                for_declared_value = formatted(cost_for_declared_value(declared_value)[0])
            else:
                cost_of_value_fiz = ""
                cost_of_value_yur = ""
                vat_value_letter = ""
                for_declared_value = ""
            simple = cost_of_simple(item_weight)
            print(simple)
            cost_of_reg_fiz = formatted(cost_of_registered(item_weight)[0])
            cost_of_reg_yur = formatted(cost_of_registered(item_weight)[1])
            vat_registered = formatted(cost_of_registered(item_weight)[2])
            context = {'form': form, 'simple': simple,
                       'cost_of_reg_fiz': cost_of_reg_fiz,
                       'cost_of_reg_yur': cost_of_reg_yur,
                       'vat_registered': vat_registered,
                       'cost_of_value_fiz': cost_of_value_fiz,
                       'cost_of_value_yur': cost_of_value_yur,
                       'vat_value_letter': vat_value_letter,
                       'for_declared_value': for_declared_value}
            return render(request, 'index.html', context)  # Внутри фиг скобок
    else:
        form = PostForm()
        return render(request, 'index.html', {'form': form})  # внутри фигурных скобок
