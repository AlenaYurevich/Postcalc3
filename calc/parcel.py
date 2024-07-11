import os
import math
from openpyxl import load_workbook
from .round_as_excel import round_as_excel
from .vat import vat
from .declared_value import cost_for_declared_value


"""
для посылок стоимость складывается из стоимости за посылку и стоимости за килограмм
Тарификация  за  массу  посылки  массой  свыше  1  кг  без  объявленной  ценности  осуществляется  с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
Тарификация  за  массу  посылки  массой  свыше  1  кг  с  объявленной  ценностью  осуществляется  с точностью  до  
десятков  граммов.  Любое  количество  граммов  округляется  до  десятков  граммов  в
большую сторону
"""


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
workbook = load_workbook(filename=file_path)
sheet = workbook.active


def formatted(num):
    if num == str(num):
        return num
    else:
        return str("{:.2f}".format(num).replace('.', ','))


def weight(item_weight, declared_value):
    if declared_value in ("нет", "", 0, "0"):
        return math.ceil(item_weight / 100) / 10
    else:
        return math.ceil(item_weight / 10) / 100


# def cost_for_declared_value(declared_value):
#     if not declared_value or declared_value in ("нет", "", 0, "0"):
#         return [0, 0]
#     fiz = round(float(declared_value) * 3 / 100, 4)
#     yur = fiz
#     return [fiz, yur]


def cost_of_parcel(item_weight, declared_value):
    price_row = []
    if item_weight <= 50000:
        if item_weight <= 1000:
            if declared_value in ("нет", "", 0, "0"):
                fiz = sheet['D29'].value
                """
                округление вверх с точностью до двух знаков
                """
                yur = sheet['H29'].value + math.ceil(sheet['H30'].value * weight(item_weight, declared_value) * 100)/100
                yur = round_as_excel(yur)
                for_declared_fiz = ''
                for_declared_yur = ''
                item_vat = vat(yur)
                yur += item_vat
                sep1 = ''
                sep2 = '/'
            else:
                fiz = sheet['D29'].value + cost_for_declared_value(declared_value)
                yur = sheet['H29'].value + sheet['H30'].value * weight(item_weight, declared_value)
                yur = round_as_excel(yur)
                for_declared_fiz = cost_for_declared_value(declared_value)
                for_declared_yur = cost_for_declared_value(declared_value) * 1.2
                item_vat = vat(yur)
                yur += item_vat
                yur += for_declared_yur
                sep1, sep2 = "/", "/"
        else:
            if declared_value in ("нет", "", 0, "0"):
                fiz = sheet['D31'].value + sheet['D32'].value * weight(item_weight, declared_value)
                yur = sheet['H29'].value + sheet['H30'].value * weight(item_weight, declared_value)
                yur = round_as_excel(yur)
                for_declared_fiz = ''
                for_declared_yur = ''
                item_vat = vat(yur)
                yur += item_vat
                sep1 = ''
                sep2 = '/'
            else:
                fiz = sheet['D31'].value + sheet['D32'].value * weight(item_weight, declared_value)
                fiz += cost_for_declared_value(declared_value)
                yur = sheet['H29'].value + sheet['H30'].value * weight(item_weight, declared_value)
                yur += cost_for_declared_value(declared_value)
                for_declared_fiz = cost_for_declared_value(declared_value)
                for_declared_yur = cost_for_declared_value(declared_value) * 1.2
                item_vat = vat(yur)
                yur += item_vat
                sep1, sep2 = "/", "/"

        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared_fiz': for_declared_fiz,
            'for_declared_yur': for_declared_yur,
            'rub': " руб.",
            'tracking': "да",
            'sep1': sep1,
            'sep2': sep2,
            }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 50 кг"
        sep1, sep2 = '', ''
        price_row.append({'fiz': fiz, 'sep1': sep1, 'sep2': sep2})
    return price_row
