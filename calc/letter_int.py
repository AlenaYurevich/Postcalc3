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
    base_cost = 10.90 if is_with_value else 0
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
    yur = round_as_excel(base_yur + item_vat_yur)

    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat_yur': item_vat_yur,
        'for_declared_fiz': for_declared if is_with_value else '',
        'for_declared_yur': for_declared if is_with_value else '',
        'rub': " руб.",
        'tracking': "да" if is_with_value else "нет",
        'sep1': "/" if is_with_value else '',
        'sep2': "/" if is_with_value else '/',
    }

    for key in rate:
        rate[key] = formatted(rate[key])

    return rate


def cost_of_letter_int(item_weight, declared_value, destination):
    if item_weight > 2000:
        limit_message = "Макс. вес 2 кг"
        return [
            [{'fiz': limit_message, 'yur': "-", 'item_vat_yur': "-"}],
            [{'fiz': limit_message, 'yur': "-", 'item_vat_yur': "-"}],
            [{'fiz': limit_message, 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
            [{'fiz': limit_message, 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
        ]
    if declared_value in ("", 0, "0"):
        return [
            [calculate_rates(item_weight, declared_value, "non_priority", False)],
            [calculate_rates(item_weight, declared_value, "priority", False)],
            [{'fiz': "-", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
            [{'fiz': "-", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}]
        ]
    else:
        if destination == 161:
            return [
                [calculate_rates(item_weight, declared_value, "non_priority", False)],
                [calculate_rates(item_weight, declared_value, "priority", False)],
                [calculate_rates(item_weight, declared_value, "non_priority", True)],
                [calculate_rates(item_weight, declared_value, "priority", True)]
            ]
        else:
            return [
                [calculate_rates(item_weight, declared_value, "non_priority", False)],
                [calculate_rates(item_weight, declared_value, "priority", False)],
                [{'fiz': "Отправления не принимаются"}],
                [calculate_rates(item_weight, declared_value, "priority", True)]
            ]
