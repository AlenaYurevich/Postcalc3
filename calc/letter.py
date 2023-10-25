import os
import math
from openpyxl import load_workbook


def weight_step(item_weight):
    return math.ceil((item_weight - 20) / 20)


def vat(num):
    return round(num * 0.2, 2)  # расчет НДС 20 %


def formatted(num):
    if num == str(num):
        return num
    else:
        return str("{:.2f}".format(num).replace('.', ','))


def cost_for_declared_value(declared_value):
    if declared_value:
        fiz = float(declared_value) * 3.6 / 100
        yur = float(declared_value) * 3 / 100
    else:
        fiz, yur = "", ""
    return [fiz, yur]


def cost_of_simple(item_weight):
    price_row = []
    if item_weight <= 2000:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')  # первый файл
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active
        fiz = sheet['B5'].value + sheet['B6'].value * weight_step(item_weight)
        yur = sheet['C5'].value + sheet['C6'].value * weight_step(item_weight)
        item_vat = vat(yur)
        yur += item_vat
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'rub': " руб."
        }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz})

    return price_row


print(cost_of_simple(2001))


def cost_of_registered(item_weight):
    price_row = []
    if item_weight <= 2000:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active
        fiz = sheet['D10'].value + sheet['D12'].value * weight_step(item_weight)
        yur = sheet['H10'].value + sheet['H12'].value * weight_step(item_weight)
        item_vat = vat(yur)
        yur += item_vat
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'rub': " руб."
        }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz})
    return price_row


def cost_of_value_letter(item_weight, declared_value):
    price_row = []
    if item_weight <= 2000:
        if declared_value:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
            workbook = load_workbook(filename=file_path)
            sheet = workbook.active
            fiz = sheet['D11'].value + sheet['D12'].value * weight_step(item_weight) + cost_for_declared_value(declared_value)[0]
            yur = sheet['H11'].value + sheet['H12'].value * weight_step(item_weight) + cost_for_declared_value(declared_value)[1]
            item_vat = vat(yur)
            yur += item_vat
            for_declared = cost_for_declared_value(declared_value)[0]
            rate = {
                'fiz': fiz,
                'yur': yur,
                'item_vat': item_vat,
                'for_declared': for_declared,
                'rub': " руб."
            }
            for i in rate:
                rate[i] = formatted(rate[i])
            price_row.append(rate)
        else:
            rate = {
                'fiz': "-",
                'yur': "-",
                'item_vat': "-",
                'for_declared': "-",
                'rub': ""
            }
            price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz})
    return price_row


print(cost_of_value_letter(20, 10))
