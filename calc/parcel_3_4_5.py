import math
from .sheets import sheet2
from .round_as_excel import round_as_excel
from .format import formatted
from .constants import notification_cost


"""
для посылок стоимость складывается из стоимости за посылку и стоимости за килограмм
Тарификация  за  массу  посылки  массой  свыше  1  кг  без  объявленной  ценности  осуществляется  с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
Тарификация  за  массу  посылки  массой  свыше  1  кг  с  объявленной  ценностью  осуществляется  с точностью  до  
десятков  граммов.  Любое  количество  граммов  округляется  до  десятков  граммов  в
большую сторону

"""


def weight(item_weight, declared_value):
    if declared_value in ("нет", "", 0):
        return math.ceil(item_weight / 100) / 10
    else:
        return math.ceil(item_weight / 10) / 100


def cost_of_parcel_declared(item_weight, declared_value, notification):
    notification = notification_cost(notification)
    if item_weight <= 1000:
        fiz = sheet2['D40'].value
    elif item_weight <= 3000:
        fiz = sheet2['D41'].value
    elif item_weight <= 5000:
        fiz = sheet2['D42'].value
    else:
        fiz = sheet2['D44'].value + sheet2['D45'].value * weight(item_weight, declared_value)
        fiz = round_as_excel(fiz)
    for_declared = ''
    if declared_value not in ("нет", "", 0, "0"):
        for_declared = round_as_excel(float(declared_value) * 0.01)
        if for_declared < 0.50:
            for_declared = 0.50
        fiz += for_declared
    if notification == notification_cost(3):
        fiz += notification * 1.2
        notification = notification * 1.2
    else:
        notification = ""
    rate = {
        'fiz': fiz,
        'for_declared': for_declared,
        'rub': " руб.",
        'notification': notification,
            }
    for i in rate:
        rate[i] = formatted(rate[i])
    return rate


def cost_of_parcel_3_4_5(item_weight, declared_value, notification):
    price_row = []
    if item_weight <= 50000:
        rate = cost_of_parcel_declared(item_weight, declared_value, notification)
        price_row.append(rate)
    else:
        fiz = "Макс. вес 50 кг"
        sep = ''
        price_row.append({'fiz': fiz, 'sep': sep})
    return price_row
