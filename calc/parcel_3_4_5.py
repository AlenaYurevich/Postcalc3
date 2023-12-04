import os
import math
from openpyxl import load_workbook
# from okr import round_as_excel


# def dec(num):
#     d = decimal.Decimal
#     return d(num).quantize(d("1.00"), decimal.ROUND_HALF_UP)
#
#
# """
# quantize - десятичные числа для отражения денежных средств, округление до двух знаков.
# decimal.ROUND_HALF_UP: 5 округляется в большую сторону
# """

def round_as_excel(num):
    # num = float(num)
    reminder = str(round(num % 1, 3))+'0000'
    if reminder[3] in '02468' and reminder[4] in '56789':
        return round(num + 0.01, 2)
    else:
        return round(num, 2)


def formatted(num):
    if num == str(num):
        return num
    else:
        return str("{:.2f}".format(num).replace('.', ','))


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


# def cost_of_parcel_simple(item_weight):
#     file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
#     workbook = load_workbook(filename=file_path, read_only=True)  # для снижения затрат ОП в режиме чтения
#     sheet = workbook.active
#     if item_weight <= 1000:
#         fiz = sheet['D42'].value
#     else:
#         if item_weight <= 3000:
#             fiz = sheet['D43'].value
#         else:
#             if item_weight <= 5000:
#                 fiz = sheet['D44'].value
#             else:
#                 fiz = sheet['D46'].value + sheet['D47'].value * weight(item_weight, declared_value=0)
#     rate = {
#         'fiz': fiz,
#         'rub': " руб."
#     }
#     for i in rate:
#         rate[i] = formatted(rate[i])
#     workbook.close()
#     return rate


def cost_of_parcel_declared(item_weight, declared_value):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
    workbook = load_workbook(filename=file_path, read_only=True)  # для снижения затрат ОП в режиме чтения
    sheet = workbook.active
    if item_weight <= 1000:
        fiz = sheet['D42'].value
    else:
        if item_weight <= 3000:
            fiz = sheet['D43'].value
        else:
            if item_weight <= 5000:
                fiz = sheet['D44'].value
            else:
                fiz = sheet['D46'].value + sheet['D47'].value * weight(item_weight, declared_value)
                fiz = round_as_excel(fiz)
    for_declared = ''
    if declared_value not in ("нет", "", 0, "0"):
        for_declared = round_as_excel(declared_value * 0.01)
        if for_declared < 0.50:
            for_declared = 0.50
        fiz += for_declared
    rate = {
        'fiz': fiz,
        'for_declared': for_declared,
        'rub': " руб."
            }
    for i in rate:
        rate[i] = formatted(rate[i])
    workbook.close()
    return rate


def cost_of_parcel_3_4_5(item_weight, declared_value):
    price_row = []
    if item_weight <= 50000:
        rate = cost_of_parcel_declared(item_weight, declared_value)
        price_row.append(rate)
    else:
        fiz = "Макс. вес 50 кг"
        sep = ''
        price_row.append({'fiz': fiz, 'sep': sep})
    return price_row


print(cost_of_parcel_3_4_5(6545, 1.55))
print(cost_of_parcel_3_4_5(6545, 50.00))
print(cost_of_parcel_3_4_5(6545, ''))
