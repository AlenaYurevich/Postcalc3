import os
import math
from openpyxl import load_workbook


"""
для отправления 1 класс стоимость добавляется за каждые последующие полные или неполные 100 г
"""


def weight_step(item_weight):
    return math.ceil((item_weight - 100) / 100)


def vat(num):
    return round(num * 0.2, 2)  # расчет НДС 20 %


def formatted(num):
    if num == str(num):
        return num
    else:
        return str("{:.2f}".format(num).replace('.', ','))


def cost_of_first_class(item_weight):
    price_row = []
    if item_weight <= 2000:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # первый файл
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active
        fiz = sheet['D23'].value + sheet['D24'].value * weight_step(item_weight)
        yur = sheet['H23'].value + sheet['H24'].value * weight_step(item_weight)
        item_vat = vat(yur)
        yur += item_vat
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared': "",
            'rub': " руб.",
            'tracking': "да"
        }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz})
    return price_row
