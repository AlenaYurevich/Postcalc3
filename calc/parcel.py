import math
from .sheets import sheet2
from .round_as_excel import round_as_excel
from .format import formatted
from .vat import vat
from .declared_value import cost_for_declared_value
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
    if declared_value in ("нет", "", 0, "0"):
        return math.ceil(item_weight / 100) / 10
    else:
        return math.ceil(item_weight / 10) / 100


def cost_of_parcel(item_weight, declared_value, notification):
    price_row = []
    notification = notification_cost(notification)
    if item_weight <= 50000:
        if item_weight <= 1000:
            if declared_value in ("нет", "", 0, "0"):
                fiz = sheet2['D27'].value
                """
                округление вверх с точностью до двух знаков
                """
                yur = sheet2['H27'].value + round((sheet2['H28'].value * weight(item_weight, declared_value)
                                                   * 100)/100, 4)
                yur = round_as_excel(yur)
                for_declared_fiz = ''
                for_declared_yur = ''
                sep1 = ''
                sep2 = '/'
            else:
                fiz = sheet2['D27'].value + cost_for_declared_value(declared_value)
                yur = sheet2['H27'].value + sheet2['H28'].value * weight(item_weight, declared_value)
                yur = round(yur, 4)
                for_declared_fiz = cost_for_declared_value(declared_value)
                yur += for_declared_fiz
                yur = round_as_excel(yur)  # округляем перед расчетом НДС
                for_declared_yur = round_as_excel(for_declared_fiz) * 1.2
                sep1, sep2 = "/", "/"
        else:
            if declared_value in ("нет", "", 0, "0"):
                fiz = sheet2['D29'].value + sheet2['D30'].value * weight(item_weight, declared_value)
                yur = sheet2['H27'].value + sheet2['H28'].value * weight(item_weight, declared_value)
                yur = round_as_excel(yur)
                for_declared_fiz = ''
                for_declared_yur = ''
                sep1 = ''
                sep2 = '/'
            else:
                fiz = sheet2['D29'].value + sheet2['D30'].value * weight(item_weight, declared_value)
                fiz += cost_for_declared_value(declared_value)
                yur = sheet2['H27'].value + sheet2['H28'].value * weight(item_weight, declared_value)
                yur = round_as_excel(yur)
                for_declared_fiz = cost_for_declared_value(declared_value)
                yur += for_declared_fiz
                yur = round_as_excel(yur)  # округляем перед расчетом НДС
                for_declared_yur = round_as_excel(for_declared_fiz * 1.2)
                sep1, sep2 = "/", "/"

        yur += notification
        notification = notification * 1.2
        fiz += notification
        if notification == 0:
            notification = ""
        item_vat_yur = vat(yur)
        yur = yur + item_vat_yur
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat_yur': item_vat_yur,
            'for_declared_fiz': for_declared_fiz,
            'for_declared_yur': for_declared_yur,
            'rub': " руб.",
            'tracking': "да",
            'sep1': sep1,
            'sep2': sep2,
            'notification': notification,
            }
        for key in rate:
            rate[key] = formatted(rate[key])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 50 кг"
        sep1, sep2 = '', ''
        price_row.append({'fiz': fiz, 'sep1': sep1, 'sep2': sep2})
    return price_row
