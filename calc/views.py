from django.shortcuts import render
from .forms import PostForm, EmsForm, TransferForm, ParcelIntForm, EmsIntForm
from .letter import cost_of_simple, cost_of_registered
from .package import cost_of_package, cost_of_value_package
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel
from .sml import cost_of_sml
from .parcel_3_4_5 import cost_of_parcel_3_4_5
from .qr_box import cost_of_parcel_qr
from .ems_points import data_of_ems
from .ems_zone import find_ems_zone
from .ems_cost import find_documents_cost, find_goods_cost
from .internal_transfer import cost_of_internal_transfer
from .parcel_int import cost_of_parcel_int
from .letter_int import cost_of_letter_int
from .package_int import cost_of_package_int
from .ems_int import cost_of_ems_int


def calculation_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            item_weight = int(request.POST.get('weight'))
            declared_value = request.POST.get('declared_value')
            notification = int(request.POST.get('notification'))
            simple = cost_of_simple(item_weight)
            registered = cost_of_registered(item_weight, notification)
            package = cost_of_package(item_weight)
            value_package = cost_of_value_package(item_weight, declared_value, notification)
            first_class = cost_of_first_class(item_weight)
            parcel = cost_of_parcel(item_weight, declared_value, notification)
            sml = cost_of_sml()
            parcel_3_4_5 = cost_of_parcel_3_4_5(item_weight, declared_value, notification)
            qr_box = cost_of_parcel_qr(item_weight, declared_value, notification)
            context = {'form': form, 'simple': simple,
                       'registered': registered,
                       'package': package,
                       'value_package': value_package,
                       'first_class': first_class,
                       'parcel': parcel,
                       'sml': sml,
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


def international_view(request):
    if request.method == "POST":
        form = ParcelIntForm(request.POST)
        if form.is_valid():
            destination = int(request.POST.get('destination'))
            item_weight = int(request.POST.get('weight'))
            declared_value = str(request.POST.get('declared_value'))
            parcel_int_cost = cost_of_parcel_int(destination, item_weight, declared_value)
            non_priority = parcel_int_cost[0]
            priority = parcel_int_cost[1]
            letter_int_cost = cost_of_letter_int(item_weight, declared_value, destination)
            non_priority_letter = letter_int_cost[0]
            priority_letter = letter_int_cost[1]
            tracked_priority = letter_int_cost[2]
            registered_non_priority = letter_int_cost[3]
            registered_priority = letter_int_cost[4]
            value_non_priority_letter = letter_int_cost[5]
            value_priority_letter = letter_int_cost[6]
            package_int_cost = cost_of_package_int(destination, item_weight)
            non_priority_pack = package_int_cost[0]
            priority_pack = package_int_cost[1]
            tracked_priority_pack = package_int_cost[2]
            registered_non_priority_pack = package_int_cost[3]
            registered_priority_pack = package_int_cost[4]
            context = {'form': form,
                       'destination': destination,
                       'item_weight': item_weight,
                       'declared_value': declared_value,
                       'non_priority': non_priority,
                       'priority': priority,
                       'non_priority_letter': non_priority_letter,
                       'tracked_priority': tracked_priority,
                       'registered_non_priority': registered_non_priority,
                       'registered_priority': registered_priority,
                       'priority_letter': priority_letter,
                       'value_non_priority_letter': value_non_priority_letter,
                       'value_priority_letter': value_priority_letter,
                       'non_priority_pack': non_priority_pack,
                       'tracked_priority_pack': tracked_priority_pack,
                       'registered_non_priority_pack': registered_non_priority_pack,
                       'registered_priority_pack': registered_priority_pack,
                       'priority_pack': priority_pack,
                       }
            return render(request, 'international.html', context)  # Внутри фиг скобок
    else:
        form = ParcelIntForm()
        return render(request, 'international.html', {'form': form})  # внутри фигурных скобок


def ems_int_view(request):
    if request.method == "POST":
        form = EmsIntForm(request.POST)
        if form.is_valid():
            destination = int(request.POST.get('destination'))
            item_weight = int(request.POST.get('weight'))
            declared_value = str(request.POST.get('declared_value'))
            ems_int_cost = cost_of_ems_int(destination, item_weight, declared_value)
            ems_documents_cost = ems_int_cost[0]
            ems_goods_cost = ems_int_cost[1]
            context = {'form': form,
                       'destination': destination,
                       'item_weight': item_weight,
                       'declared_value': declared_value,
                       'ems_documents_cost': ems_documents_cost,
                       'ems_goods_cost': ems_goods_cost,
                       }
            return render(request, 'ems_international.html', context)  # Внутри фиг скобок
    else:
        form = EmsIntForm()
        return render(request, 'ems_international.html', {'form': form})  # внутри фигурных скобок


def about_view(request):
    return render(request, 'about.html')


def page_not_found_view(request):
    return render(request, '404/404.html', status=404)
