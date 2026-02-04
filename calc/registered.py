import math
from .sheets import sheet2
from .vat import vat
from .format import formatted
from .constants import notification_cost2


def weight_step(weight):
    return math.ceil((weight - 20) / 20)


def registered_letter(item_weight):
    MAX_WEIGHT = 2000  # грамм
    if item_weight > MAX_WEIGHT:
        return {'fiz': "Макс. вес 2 кг"}
    fiz = sheet2['D10'].value + sheet2['D11'].value * weight_step(item_weight)
    yur = sheet2['H10'].value + sheet2['H11'].value * weight_step(item_weight)
    yur += vat(yur)
    notification2 = notification_cost2(1)
    notification3 = notification_cost2(2)
    notification4 = notification_cost2(3)
    rate = {
        'fiz': fiz,
        'yur': yur,
        'notification2': notification2,
        'fiz2': fiz + notification2,
        'yur2': yur + notification2,
        'notification3': notification3,
        'fiz3': fiz + notification3,
        'yur3': yur + notification3,
        'notification4': notification4,
        'fiz4': fiz + notification4,
        'yur4': yur + notification4,
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    return rate
