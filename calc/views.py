from django.shortcuts import render
from .forms import PostForm, EmsForm, TransferForm
from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel
from .parcel_3_4_5 import cost_of_parcel_3_4_5
from .qr_box import cost_of_parcel_qr
from .ems_points import data_of_ems
from .ems_zone import find_ems_zone
from .ems_cost import find_documents_cost, find_goods_cost
from .internal_transfer import cost_of_internal_transfer


def calculation_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            item_weight = int(request.POST.get('weight'))
            declared_value = request.POST.get('declared_value')
            notification = int(request.POST.get('notification'))
            simple = cost_of_simple(item_weight)
            registered = cost_of_registered(item_weight, notification)
            value_letter = cost_of_value_letter(item_weight, declared_value, notification)
            first_class = cost_of_first_class(item_weight)
            parcel = cost_of_parcel(item_weight, declared_value, notification)
            parcel_3_4_5 = cost_of_parcel_3_4_5(item_weight, declared_value, notification)
            qr_box = cost_of_parcel_qr(item_weight, declared_value, notification)
            context = {'form': form, 'simple': simple,
                       'registered': registered,
                       'value_letter': value_letter,
                       'first_class': first_class,
                       'parcel': parcel,
                       'parcel_3_4_5': parcel_3_4_5,
                       'qr_box': qr_box,
                       'notification': notification
                       }
            return render(request, 'index.html', context)  # Внутри фигурных скобок
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
            declared_value = str(request.POST.get('declared_value'))
            delivery = float(request.POST.get('delivery'))
            notification = int(request.POST.get('notification'))
            fragile = str(request.POST.get('fragile'))
            zone1 = data_of_ems(departure, destination, item_weight, declared_value)[0]
            zone2 = data_of_ems(departure, destination, item_weight, declared_value)[1]
            ems_zone = find_ems_zone(zone1, zone2)
            ems_documents_cost = find_documents_cost(ems_zone, item_weight, declared_value, delivery, notification,
                                                     fragile)
            ems_goods_cost = find_goods_cost(ems_zone, item_weight, declared_value, delivery, notification, fragile)
            post_office_ems_documents_cost = ems_documents_cost[0]
            home_ems_documents_cost = ems_documents_cost[1]
            post_office_ems_goods_cost = ems_goods_cost[0]
            home_ems_goods_cost = ems_goods_cost[1]
            context = {'form': form,
                       'departure': departure,
                       'destination': destination,
                       'item_weight': item_weight,
                       'declared_value': declared_value,
                       'delivery': delivery,
                       'notification': notification,
                       'fragile': fragile,
                       'post_office_ems_documents_cost': post_office_ems_documents_cost,
                       'home_ems_documents_cost': home_ems_documents_cost,
                       'post_office_ems_goods_cost': post_office_ems_goods_cost,
                       'home_ems_goods_cost': home_ems_goods_cost,
                       }
            return render(request, 'ems_express_dostavka.html', context)  # Внутри фиг скобок
    else:
        form = EmsForm()
        return render(request, 'ems_express_dostavka.html', {'form': form})  # внутри фигурных скобок


def internal_transfer_view(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = float(request.POST.get('amount'))
            internal_transfer_cost = cost_of_internal_transfer(amount)
            context = {'form': form,
                       'amount': amount,
                       'internal_transfer_cost': internal_transfer_cost
                       }
            return render(request, 'internal_transfer.html', context)  # Внутри фиг скобок
    else:
        form = TransferForm()
        return render(request, 'internal_transfer.html', {'form': form})  # внутри фигурных скобок


def about_view(request):
    return render(request, 'about.html')


def page_not_found_view(request):
    return render(request, '404/404.html', status=404)
