import os
from openpyxl import load_workbook
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/ems_rates.xlsx')
wb = load_workbook(filename=file_path)
sheet = wb.active


def find_column_letter(zone):
    letters = ' DEFGH'  # name of columns correspond to tariff zones 1-5
    return letters[zone]


def find_documents_table_row(weight):
    if weight <= 1000:
        return 10
    elif weight <= 2000:
        return 11


def find_goods_table_row(weight):
    """
    Находит номер строки таблицы товаров для заданного веса.
    Args:
        weight (int): Вес товара в граммах.
    Returns:
        int: Номер строки таблицы товаров.
    """
    # Диапазоны весов и соответствующие номера строк
    ranges = [
        (0, 1000, 13),
        (1001, 2000, 14),
        (2001, 3000, 15),
        (3001, 5000, 16),
        (5001, 10000, 17),
        (10001, 15000, 18),
        (15001, 20000, 19),
        (20001, 25000, 20),
        (25001, 30000, 21),
        (30001, 35000, 22),
        (35001, 40000, 23),
        (40001, 45000, 24),
        (45001, 50000, 25),
    ]

    # Двоичный поиск для нахождения соответствующего диапазона
    left, right = 0, len(ranges) - 1
    while left <= right:
        mid = (left + right) // 2
        min_weight, max_weight, row_number = ranges[mid]

        if min_weight <= weight <= max_weight:
            return row_number
        elif weight < min_weight:
            right = mid - 1
        else:
            left = mid + 1

    # Если вес выходит за пределы последнего диапазона
    return None


def find_table_row(weight, item):
    """
    Находит номер строки таблицы для заданного веса и типа товара.
    Args:
        weight (int): Вес товара в граммах.
        item (str): Тип товара ('documents' или 'goods').
    Returns:
        int: Номер строки в таблице.
    """
    if item == "documents":
        return find_documents_table_row(weight)
    elif item == "goods":
        return find_goods_table_row(weight)
    else:
        raise ValueError("Неизвестный тип товара.")


def cost_for_declared_value(declared_value):
    if not declared_value or declared_value in ("нет", "", 0, "0"):
        return [0, 0]
    fiz = round(float(declared_value) * 3 / 100, 4)
    yur = fiz
    return [fiz, yur]


def find_item_cost(zone, weight, declared_value, item, reception_place):
    x = find_column_letter(zone)
    if reception_place == 'post_office':
        row = find_table_row(weight, item)
    else:
        row = find_table_row(weight, item) + 18

    if declared_value:
        fiz = sheet[f"{x}{row}"].value
        yur = fiz
        fiz += cost_for_declared_value(declared_value)[0]
        yur += cost_for_declared_value(declared_value)[1]
        yur = round_as_excel(yur)
        for_declared = cost_for_declared_value(declared_value)[1] * 1.2
    else:
        fiz = sheet[f"{x}{row}"].value
        yur = fiz
        for_declared = "-"

    item_vat = round_as_excel(vat(yur))
    fiz += item_vat
    yur += item_vat

    return [{
        "fiz": formatted(fiz),
        "yur": formatted(yur),
        "item_vat": formatted(item_vat),
        "for_declared": formatted(for_declared),
    }]


def find_documents_cost(zone, weight, declared_value):
    if weight > 2000:
        return [
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat': "-", 'for_declared': "-"}],
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat': "-", 'for_declared': "-"}],
        ]
    return [find_item_cost(zone, weight, declared_value, 'documents', 'post_office'),
            find_item_cost(zone, weight, declared_value, 'documents', 'home')]


def find_goods_cost(zone, weight, declared_value):
    if weight > 50000:
        return [
            [{'fiz': "Макс. вес 50 кг", 'yur': "-", 'item_vat': "-", 'for_declared': "-"}],
            [{'fiz': "Макс. вес 50 кг", 'yur': "-", 'item_vat': "-", 'for_declared': "-"}],
        ]
    return [find_item_cost(zone, weight, declared_value, 'goods', 'post_office'),
            find_item_cost(zone, weight, declared_value, 'goods', 'home')]
