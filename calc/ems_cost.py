import os
from openpyxl import load_workbook
from .vat import vat
from .round_as_excel import round_as_excel


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
        return 10
    elif weight <= 2000:
        return 11


def find_goods_table_row(weight):
    if weight <= 1000:
        return 13
    elif weight <= 2000:
        return 14
    elif weight <= 3000:
        return 15
    elif weight <= 5000:
        return 16
    elif weight <= 10000:
        return 17
    elif weight <= 15000:
        return 18
    elif weight <= 20000:
        return 19
    elif weight <= 25000:
        return 20
    elif weight <= 30000:
        return 21
    elif weight <= 35000:
        return 22
    elif weight <= 40000:
        return 23
    elif weight <= 45000:
        return 24
    elif weight <= 50000:
        return 25


def cost_for_declared_value(declared_value):
    if declared_value not in ("нет", "", 0, "0"):
        fiz = float(declared_value) * 3.6 / 100
        fiz = round_as_excel(fiz)
        yur = float(declared_value) * 3 / 100
        yur = round(yur, 4)
    else:
        fiz, yur = 0, 0
    return [fiz, yur]


def find_item_cost(zone, weight, declared_value, item, reception_place):
    price_row = []
    y = 0
    if reception_place == 'post_office':
        if item == 'documents':
            y = find_documents_table_row(weight)
        elif item == 'goods':
            y = find_goods_table_row(weight)
    elif reception_place == 'home':
        if item == 'documents':
            y = find_documents_table_row(weight) + 18
        elif item == 'goods':
            y = find_goods_table_row(weight) + 18
    if declared_value not in ("нет", "", 0, "0"):
        x = find_column_letter(zone)
        fiz = sheet[str(x + str(y))].value * 1.2
        yur = sheet[str(x + str(y))].value
        fiz += cost_for_declared_value(declared_value)[0]
        yur += cost_for_declared_value(declared_value)[1]
        yur = round_as_excel(yur)
        item_vat = round_as_excel(vat(yur))
        yur += item_vat
        for_declared = cost_for_declared_value(declared_value)[1] * 1.2
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared': for_declared
                    }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    else:
        x = find_column_letter(zone)
        fiz = sheet[str(x + str(y))].value * 1.2
        yur = sheet[str(x + str(y))].value
        item_vat = vat(yur)
        yur += item_vat
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared': "-"
        }
        for i in rate:
            rate[i] = formatted(rate[i])
        price_row.append(rate)
    return price_row


def find_ems_cost(zone, weight, declared_value):
    if weight > 2000:
        post_office_documents_price_row = [{
            'fiz': "Макс. вес 2 кг",
            'yur': "-",
            'item_vat': "-",
            'for_declared': "-"
        }]
        home_documents_price_row = [{
            'fiz': "Макс. вес 2 кг",
            'yur': "-",
            'item_vat': "-",
            'for_declared': "-"
        }]
    else:
        post_office_documents_price_row = find_item_cost(zone, weight, declared_value, 'documents', 'post_office')
        home_documents_price_row = find_item_cost(zone, weight, declared_value, 'documents', 'home')
    if weight > 50000:
        post_office_goods_price_row = [{
            'fiz': "Макс. вес 50 кг",
            'yur': "-",
            'item_vat': "-",
            'for_declared': "-"
        }]
    else:
        post_office_goods_price_row = find_item_cost(zone, weight, declared_value, 'goods', 'post_office')
    return post_office_documents_price_row, home_documents_price_row, post_office_goods_price_row
