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


def find_documents_table_row(weight):
    if weight <= 1000:
        return '10'
    elif weight <= 2000:
        return '11'


def find_goods_table_row(weight):
    if weight <= 1000:
        return '13'
    elif weight <= 2000:
        return '14'
    elif weight <= 3000:
        return '15'
    elif weight <= 5000:
        return '16'
    elif weight <= 10000:
        return '17'
    elif weight <= 15000:
        return '18'
    elif weight <= 20000:
        return '19'
    elif weight <= 25000:
        return '20'
    elif weight <= 30000:
        return '21'
    elif weight <= 35000:
        return '22'
    elif weight <= 40000:
        return '23'
    elif weight <= 45000:
        return '24'
    elif weight <= 50000:
        return '25'


def find_ems_documents_cost(zone, weight):
    price_row = []
    if weight <= 2000:
        x = find_column_letter(zone)
        yur = sheet[str(x + find_documents_table_row(weight))].value
        item_vat = vat(yur)
        yur += item_vat
        rate = {
            'fiz': yur,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared': ""
                    }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        fiz = "Макс. вес 2 кг"
        price_row.append({'fiz': fiz})
    return price_row

