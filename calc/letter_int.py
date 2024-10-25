from .sheets import sheet4
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .declared_value import cost_for_declared_value


def find_letter_table_row(weight):
    """
    Находит номер строки таблицы для заданного веса.
    Args:
        weight (int): Вес письма в граммах.
    Returns:
        int: Номер строки таблицы товаров.
    """
    # Диапазоны веса и соответствующие номера строк
    ranges = [
        (0, 20, 10),
        (21, 50, 11),
        (51, 100, 12),
        (101, 250, 13),
        (251, 500, 14),
        (501, 1000, 15),
        (1001, 2000, 16),
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


def find_column_letter(priority):
    if priority == "non_priority":
        return 'D'
    elif priority == "priority":
        return 'E'
    return None


def find_simple_letter_int_cost(item_weight, priority):
    price_row = []
    col = find_column_letter(priority)
    row = find_letter_table_row(item_weight)
    fiz = sheet4[f"{col}{row}"].value
    yur = fiz
    sep1 = ''
    sep2 = '/'
    item_vat_yur = vat(yur)
    fiz = round_as_excel(fiz + item_vat_yur)
    yur = round_as_excel(yur + item_vat_yur)
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat_yur': item_vat_yur,
        'rub': " руб.",
        'tracking': "нет",
        'sep1': sep1,
        'sep2': sep2,
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    price_row.append(rate)
    return price_row


def find_value_letter_int_cost(item_weight, declared_value, priority):
    price_row = []
    col = find_column_letter(priority)
    row = find_letter_table_row(item_weight)
    fiz = 10.90 + sheet4[f"{col}{row}"].value
    yur = fiz
    for_declared_fiz = cost_for_declared_value(declared_value)
    fiz += cost_for_declared_value(declared_value)
    yur += cost_for_declared_value(declared_value)
    yur = round_as_excel(yur)
    for_declared_yur = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
    sep1, sep2 = "/", "/"
    item_vat_yur = vat(yur)
    fiz = round_as_excel(fiz + item_vat_yur)
    yur = round_as_excel(yur + item_vat_yur)
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat_yur': item_vat_yur,
        'for_declared_fiz': for_declared_fiz,
        'for_declared_yur': for_declared_yur,
        'rub': " руб.",
        'tracking': "да",
        'sep1': sep1,
        'sep2': sep2,
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    price_row.append(rate)
    return price_row


def cost_of_letter_int(item_weight, declared_value):
    if item_weight > 2000:
        return [
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat_yur': "-"}],
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat_yur': "-"}],
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
        ]
    return [find_simple_letter_int_cost(item_weight, "non_priority"),
            find_simple_letter_int_cost(item_weight, "priority"),
            find_value_letter_int_cost(item_weight, declared_value, "non_priority"),
            find_value_letter_int_cost(item_weight, declared_value, "priority")]
