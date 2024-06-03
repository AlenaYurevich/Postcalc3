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
        fiz = float(declared_value) * 3 / 100
        fiz = round_as_excel(fiz)
        yur = float(declared_value) * 3 / 100
        yur = round_as_excel(yur)
    else:
        fiz, yur = 0, 0
    return [fiz, yur]


def find_the_row(weight):
    rows = []
    row = find_documents_table_row(weight)
    rows.append(row)
    row = find_goods_table_row(weight)
    rows.append(row)
    row = find_documents_table_row(weight) + 18
    rows.append(row)
    row = find_goods_table_row(weight) + 18
    rows.append(row)
    return rows


print(find_the_row(500))


def find_item_cost(zone, weight, declared_value):
    final_price_row = []
    price_rows = find_the_row(weight)
    x = find_column_letter(zone)
    if declared_value not in ("нет", "", 0, "0"):
        fiz = sheet[str(x + str(price_rows[0]))].value
        yur = sheet[str(x + str(price_rows[0]))].value
        fiz += cost_for_declared_value(declared_value)[0]
        yur += cost_for_declared_value(declared_value)[1]
        yur = round_as_excel(yur)
        item_vat = round_as_excel(vat(yur))
        fiz += item_vat
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
        final_price_row.append(rate)
    else:
        x = find_column_letter(zone)
        fiz = sheet[str(x + str(price_rows[0]))].value
        yur = sheet[str(x + str(price_rows[0]))].value
        item_vat = vat(yur)
        fiz += item_vat
        yur += item_vat
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'for_declared': "-"
        }
        for i in rate:
            rate[i] = formatted(rate[i])
        final_price_row.append(rate)
    return final_price_row


def find_ems_cost(zone, weight, declared_value):
    rates = []
    if weight <= 2000:
        rates = find_item_cost(zone, weight, declared_value)
        post_office_documents_price_row = rates
        home_documents_price_row = rates
    else:
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
    if weight >= 50000:
        post_office_goods_price_row = [{
            'fiz': "Макс. вес 50 кг",
            'yur': "-",
            'item_vat': "-",
            'for_declared': "-"
        }]
        home_goods_price_row = [{
            'fiz': "Макс. вес 50 кг",
            'yur': "-",
            'item_vat': "-",
            'for_declared': "-"
        }]
    else:
        post_office_goods_price_row = rates
        home_goods_price_row = rates
    return post_office_documents_price_row, home_documents_price_row, post_office_goods_price_row, home_goods_price_row
