from .sheets import sheet4
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .declared_value import cost_for_declared_value
from .constants import TRACKED_RATE, REGISTERED_RATE, VALUE_RATE


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

    for min_weight, max_weight, row_number in ranges:
        if min_weight <= weight <= max_weight:
            return row_number
    return None


def find_column_letter(priority):
    """Возвращает колонку таблицы в зависимости от приоритета."""
    columns = {
        "non_priority": 'D',
        "priority": 'E'
    }
    return columns.get(priority)


def calculate_rates(item_weight, declared_value, priority, is_with_value):
    """Рассчитывает стоимость писем с учетом заданных параметров."""
    base_cost = VALUE_RATE if is_with_value else 0
    col = find_column_letter(priority)
    row = find_letter_table_row(item_weight)

    if row is None:
        return None

    base_fiz = sheet4[f"{col}{row}"].value + base_cost
    base_yur = base_fiz

    if is_with_value:
        for_declared = cost_for_declared_value(declared_value)
        base_fiz += for_declared
        base_yur = base_fiz
        for_declared = round_as_excel(for_declared * 1.2)
    else:
        for_declared = ''
    item_vat_yur = vat(base_yur)
    fiz = round_as_excel(base_fiz + item_vat_yur)
    yur = fiz

    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat_yur': item_vat_yur,
        'for_declared': for_declared if is_with_value else '',
        'rub': " руб.",
        'tracking': "да" if is_with_value else "нет",
    }

    for key in rate:
        rate[key] = formatted(rate[key])

    return rate


def calculate_registered(item_weight, priority, is_registered):
    add_cost = REGISTERED_RATE if is_registered else TRACKED_RATE  # заказное или отслеживаемое письмо
    col = find_column_letter(priority)
    row = find_letter_table_row(item_weight)
    fiz = sheet4[f"{col}{row}"].value + add_cost
    item_vat = vat(fiz)
    fiz = round_as_excel(fiz + item_vat)
    yur = fiz
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat': item_vat,
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    return rate


def cost_of_letter_int(item_weight, declared_value, destination):
    if item_weight > 2000:
        limit_message = "Макс. вес 2 кг"
        return [
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
        ]
    else:
        simple_non_priority = calculate_rates(item_weight, declared_value, "non_priority", False)
        simple_priority = calculate_rates(item_weight, declared_value, "priority", False)
        tracked_priority = calculate_registered(item_weight, "priority", False)
        registered_non_priority = {'fiz': "Отправления не принимаются"}
        registered_priority = calculate_registered(item_weight, "priority", True)
        declared_non_priority = {'fiz': "-", 'yur': "-"}
        declared_priority = {'fiz': "-", 'yur': "-"}
    if declared_value not in ("", "0"):
        declared_priority = calculate_rates(item_weight, declared_value, "priority", True)
        if destination == 161:
            registered_non_priority = calculate_registered(item_weight, "non_priority", True)
            declared_non_priority = calculate_rates(item_weight, declared_value, "priority", True)
        else:
            declared_non_priority = {'fiz': "Отправления не принимаются"}
    else:
        if destination == 161:
            registered_non_priority = calculate_registered(item_weight, "non_priority", True)
    return [[simple_non_priority],
            [simple_priority],
            [tracked_priority],
            [registered_non_priority],
            [registered_priority],
            [declared_non_priority],
            [declared_priority]
            ]
