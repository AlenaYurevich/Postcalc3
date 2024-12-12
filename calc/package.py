import math
from .sheets import sheet2
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .constants import notification_cost
from .declared_value import cost_for_declared_value


def weight_step(weight):
    return math.ceil((weight - 20) / 20)


def cost_of_package(item_weight):
    price_row = []
    if item_weight <= 2000:
        fiz = sheet2['D13'].value + sheet2['D16'].value * weight_step(item_weight)
        yur = sheet2['H13'].value + sheet2['H16'].value * weight_step(item_weight)
        item_vat = vat(yur)
        yur += item_vat
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared': "",
            'rub': " руб.",
            'tracking': "нет"
        }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz})
    return price_row


"""
заказное письмо, заказная бандероль, заказной мелкий пакет
"""


def cost_of_registered(item_weight, notification):
    price_row = []
    notification = notification_cost(notification)
    if item_weight <= 2000:
        fiz = sheet2['D10'].value + sheet2['D11'].value * weight_step(item_weight)
        yur = sheet2['H10'].value + sheet2['H11'].value * weight_step(item_weight)
        fiz += notification * 1.2
        yur += notification
        notification = notification * 1.2
        if notification == 0:
            notification = ""
        item_vat = vat(yur)
        yur += item_vat
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared': "",
            'rub': " руб.",
            'tracking': "да",
            'notification': notification
        }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz})
    return price_row


"""
Мелкий пакет с объявленной ценностью
"""


def cost_of_value_package(item_weight, declared_value, notification):
    price_row = []
    notification = notification_cost(notification)
    if item_weight <= 2000:
        if declared_value not in ("нет", "", 0, "0"):
            fiz = sheet2['D15'].value + sheet2['D16'].value * weight_step(item_weight)\
                                     + round_as_excel(cost_for_declared_value(declared_value)) * 1.2
            yur = sheet2['H15'].value + sheet2['H16'].value * weight_step(item_weight)\
                                      + cost_for_declared_value(declared_value)
            fiz += notification * 1.2
            yur += notification
            notification = notification * 1.2
            if notification == 0:
                notification = ""
            item_vat = vat(yur)
            yur += item_vat
            for_declared = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
            rate = {
                'fiz': fiz,
                'yur': yur,
                'item_vat': item_vat,
                'for_declared': for_declared,
                'rub': " руб.",
                'tracking': "да",
                'sep': '/',
                'notification': notification
            }
            for i in rate:
                rate[i] = formatted(rate[i])
            price_row.append(rate)
        else:
            rate = {
                'fiz': "",
                'yur': "",
                'item_vat': "",
                'for_declared': "",
                'rub': "",
                'sep': "",
                'notification': ""
            }
            price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz, 'sep': ''})
    return price_row
