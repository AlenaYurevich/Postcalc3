import os
import math
from openpyxl import load_workbook


def weight_step(item_weight):
    return math.ceil((item_weight - 20) / 20)


def cost_of_simple(item_weight):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    fiz = sheet['B5'].value + sheet['B6'].value * weight_step(item_weight)
    yur = (sheet['C5'].value + sheet['C6'].value * weight_step(item_weight)) * 1.2
    return [fiz, yur]
