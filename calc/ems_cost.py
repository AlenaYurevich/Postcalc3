import os
from openpyxl import load_workbook
from .vat import vat


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/ems_rates.xlsx')
wb = load_workbook(filename=file_path)
sheet = wb.active


def find_column_letter(zone):
    letters = ' DEFGH'  # name of columns correspond to tariff zones 1-5
    return letters[zone]


def formatted(num):
    if num == str(num):
        return num
    else:
        return str("{:.2f}".format(num).replace('.', ','))


def find_ems_documents_cost(zone, item_weight):
    x = find_column_letter(zone)
    if item_weight <= 1000:
        yur = sheet[str(x + '10')].value
    elif item_weight <= 2000:
        yur = sheet[str(x + '11')].value
    else:
        return 'документы до 2 кг включительно'
    item_vat = vat(yur)
    yur += item_vat
    return formatted(yur)


print(find_ems_documents_cost(5, 2500))
