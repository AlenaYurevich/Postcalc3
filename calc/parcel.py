import os
import math
from openpyxl import load_workbook
from decimal import Decimal


"""
для посылок стоимость складывается из стоимости за посылку и стоимости за килограмм
Тарификация  за  массу  посылки  массой  свыше  1  кг  без  объявленной  ценности  осуществляется  с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
Тарификация  за  массу  посылки  массой  свыше  1  кг  с  объявленной  ценностью  осуществляется  с точностью  до  
десятков  граммов.  Любое  количество  граммов  округляется  до  десятков  граммов  в
большую сторону

"""


def dec(num):
    return Decimal(num).quantize(Decimal("1.00"))  # десятичные числа для отражения денежных средств


def vat(num):
    return dec(num * dec(0.2))


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


def cost_for_declared_value(declared_value):
    fiz = dec(float(declared_value) * 3 / 100)
    yur = dec(float(declared_value) * 3 / 100)
    return [fiz, yur]


def cost_of_parcel(item_weight, declared_value):
    price_row = []
    if item_weight <= 50000:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active
        if item_weight <= 1000:
            if declared_value in ("нет", "", 0, "0"):
                fiz = sheet['D29'].value
                """
                округление вверх с точностью до двух знаков
                """
                yur = sheet['H29'].value + math.ceil(sheet['H30'].value * weight(item_weight, declared_value) * 100)/100
                yur = dec(yur)
                for_declared_fiz = ''
                for_declared_yur = ''
                item_vat = vat(yur)
                yur += item_vat
            else:
                fiz = sheet['D29'].value + cost_for_declared_value(declared_value)[0]
                yur = sheet['H29'].value + sheet['H30'].value * weight(item_weight, declared_value)
                yur = dec(yur)
                for_declared_fiz = cost_for_declared_value(declared_value)[0]
                for_declared_yur = cost_for_declared_value(declared_value)[1]
                for_declared_yur += vat(for_declared_yur)
                print(for_declared_yur, "за объявленную ценность")
                item_vat = vat(yur)
                print(item_vat, "ндс")
                yur += item_vat
                yur += for_declared_yur
        else:
            if declared_value in ("нет", "", 0, "0"):
                fiz = sheet['D31'].value + sheet['D32'].value * weight(item_weight, declared_value)
                yur = sheet['H29'].value + sheet['H30'].value * weight(item_weight, declared_value)
                yur = dec(yur)
                for_declared_fiz = ''
                for_declared_yur = ''
                item_vat = vat(yur)
                yur += item_vat
            else:
                fiz = sheet['D31'].value + sheet['D32'].value * weight(item_weight, declared_value)
                fiz = dec(fiz)
                fiz += cost_for_declared_value(declared_value)[0]
                yur = sheet['H29'].value + sheet['H30'].value * weight(item_weight, declared_value)
                yur = dec(yur)
                yur += cost_for_declared_value(declared_value)[1]
                for_declared_fiz = cost_for_declared_value(declared_value)[0]
                for_declared_yur = cost_for_declared_value(declared_value)[1]
                for_declared_yur += vat(for_declared_yur)
                item_vat = vat(yur)
                yur += item_vat

        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared_fiz': for_declared_fiz,
            'for_declared_yur': for_declared_yur,
            'rub': " руб.",
            'tracking': "да",
            'sep': '/'
            }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 50 кг"
        sep = ''
        price_row.append({'fiz': fiz, 'sep': sep})

    return price_row


print(cost_of_parcel(500, 0))
print(cost_of_parcel(500, 1.25))
