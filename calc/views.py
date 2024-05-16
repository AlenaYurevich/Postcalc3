# import requests
# from django.http import HttpResponseRedirect
from django.shortcuts import render
# from openpyxl import load_workbook
from .forms import PostForm, EmsForm
from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel
from .parcel_3_4_5 import cost_of_parcel_3_4_5
from .ems_points import data_of_ems
from .ems_zone import find_ems_zone


# def read_letter_from_exel(filepath):
#     price_list = []
#     workbook = load_workbook(filename=filepath)
#     sheet = workbook.active
#
#     for row in sheet.iter_rows(min_row=3, values_only=True):
#         item, cost_fiz, cost_yur = row
#         rates = {
#             'item': item,
#             'cost_fiz': cost_fiz,
#             'cost_yur': cost_yur
#                     }
#         price_list.append(rates)
#     return price_list


def calculation_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            item_weight = int(request.POST.get('weight'))
            declared_value = request.POST.get('declared_value')
            simple = cost_of_simple(item_weight)
            registered = cost_of_registered(item_weight)
            value_letter = cost_of_value_letter(item_weight, declared_value)
            first_class = cost_of_first_class(item_weight)
            parcel = cost_of_parcel(item_weight, declared_value)
            parcel_3_4_5 = cost_of_parcel_3_4_5(item_weight, declared_value)
            context = {'form': form, 'simple': simple,
                       'registered': registered,
                       'value_letter': value_letter,
                       'first_class': first_class,
                       'parcel': parcel,
                       'parcel_3_4_5': parcel_3_4_5,
                       }
            return render(request, 'index.html', context)  # Внутри фиг скобок
    else:
        form = PostForm()
        return render(request, 'index.html', {'form': form})  # внутри фигурных скобок


def ems_view(request):
    if request.method == "POST":
        form = EmsForm(request.POST)
        if form.is_valid():
            departure = request.POST.get('departure')
            destination = request.POST.get('destination')
            item_weight = int(request.POST.get('weight'))
            declared_value = request.POST.get('declared_value')
            ems = data_of_ems(departure, destination, item_weight, declared_value)
            zone1 = data_of_ems(departure, destination, item_weight, declared_value)[0]
            zone2 = data_of_ems(departure, destination, item_weight, declared_value)[1]
            ems_zone = find_ems_zone(zone1, zone2)
            context = {'form': form,
                       'departure': departure,
                       'destination': destination,
                       'item_weight': item_weight,
                       'declared_value': declared_value,
                       'ems': ems,
                       'ems_zone': ems_zone
                       }
            return render(request, 'ems_express_dostavka.html', context)  # Внутри фиг скобок
    else:
        form = EmsForm()
        return render(request, 'ems_express_dostavka.html', {'form': form})  # внутри фигурных скобок
