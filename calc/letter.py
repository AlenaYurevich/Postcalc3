import os
import math
from openpyxl import load_workbook


def weight_step(item_weight):
    return math.ceil((item_weight - 20) / 20)


def vat(num):
    return round(num * 0.2, 2)  # расчет НДС 20 %


def cost_of_simple(item_weight):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    fiz = sheet['B5'].value + sheet['B6'].value * weight_step(item_weight)
    yur = sheet['C5'].value + sheet['C6'].value * weight_step(item_weight)
    yur += vat(yur)
    return [fiz, yur, vat(yur)]


def cost_of_registered(item_weight):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    fiz = sheet['D10'].value + sheet['D18'].value * weight_step(item_weight)
    yur = sheet['H10'].value + sheet['H18'].value * weight_step(item_weight)
    yur += vat(yur)
    return [fiz, yur, vat(yur)]
