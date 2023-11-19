import os
import math
from openpyxl import load_workbook
from decimal import Decimal


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
    if declared_value in ("нет", "", 0):
        return math.ceil(item_weight / 100) / 10
    else:
        return math.ceil(item_weight / 10) / 100


def cost_of_parcel_simple(item_weight):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
    workbook = load_workbook(filename=file_path)
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
                fiz = sheet['D46'].value + sheet['D47'].value * weight(item_weight, declared_value=0)
    rate = {
        'fiz': fiz,
        'rub': " руб.",
        'tracking': "да",
    }
    for i in rate:
        rate[i] = formatted(rate[i])
        print(rate)
        return rate


def cost_of_parcel_declared(item_weight, declared_value):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
    workbook = load_workbook(filename=file_path)
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
    for_declared = declared_value * 0.01
    fiz += for_declared
    rate = {
        'fiz': fiz,
        'for_declared': for_declared,
        'rub': " руб.",
        'tracking': "да"
    }
    for i in rate:
        rate[i] = formatted(rate[i])
    print(rate)
    return rate


def cost_of_parcel_3_4_5(item_weight, declared_value):
    price_row = []
    if item_weight <= 50000:
        if declared_value in ("нет", "", 0, "0"):
            rate = cost_of_parcel_simple(item_weight)
        else:
            rate = cost_of_parcel_declared(item_weight, declared_value)
        price_row.append(rate)
    else:
        fiz = "Макс. вес 50 кг"
        sep = ''
        price_row.append({'fiz': fiz, 'sep': sep})
    return price_row


print(cost_of_parcel_3_4_5(500, 0))
print(cost_of_parcel_3_4_5(500, 1.25))
