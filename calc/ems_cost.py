from .sheets import sheet6
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .declared_value import cost_for_declared_value
from .constants import notification_cost


def find_column_letter(zone):
    letters = ' DEFGH'  # name of columns correspond to tariff zones 1-5
    return letters[zone]


def find_table_row(weight):
    """
    Находит номер строки таблицы товаров для заданного веса.
    Args:
        weight (int): Вес товара в граммах.
    Returns:
        int: Номер строки таблицы товаров.
    """
    # Диапазоны весов и соответствующие номера строк
    ranges = [
        (0, 1000, 10),
        (1001, 2000, 11),
        (2001, 3000, 12),
        (3001, 5000, 13),
        (5001, 10000, 14),
        (10001, 15000, 15),
        (15001, 20000, 16),
        (20001, 25000, 17),
        (25001, 30000, 18),
        (30001, 35000, 19),
        (35001, 40000, 20),
        (40001, 45000, 21),
        (45001, 50000, 22),
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


def fragile_cost(fragile):
    return 1 if fragile == "None" else 1.50


def find_item_cost(zone, weight, declared_value, reception_place, delivery, notification, fragile):
    x = find_column_letter(zone)
    notification = notification_cost(notification)
    for_fragile = fragile_cost(fragile)
    if reception_place == 'post_office':
        row = find_table_row(weight)
    else:
        row = find_table_row(weight) + 14
    delivery2 = delivery
    if delivery == 2.5:
        delivery2 = 2
    if declared_value:
        fiz = sheet6[f"{x}{row}"].value * delivery
        yur = sheet6[f"{x}{row}"].value * delivery2
        yur += cost_for_declared_value(declared_value)
        for_declared_yur = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
        fiz += cost_for_declared_value(declared_value) * 1.2
    else:
        fiz = sheet6[f"{x}{row}"].value * delivery
        yur = sheet6[f"{x}{row}"].value * delivery2
        for_declared_yur = "-"
    fiz *= for_fragile
    yur *= for_fragile
    fiz += notification
    yur += notification
    notification = notification * 1.2
    if notification == 0:
        notification = ""
    item_vat_yur = round_as_excel(vat(yur))
    yur = round_as_excel(yur + item_vat_yur)
    return [{
        "fiz": formatted(fiz),
        "yur": formatted(yur),
        "item_vat": formatted(item_vat_yur),
        "for_declared_yur": formatted(for_declared_yur),
        'notification': formatted(notification)
    }]


def find_goods_cost(zone, weight, declared_value, delivery, notification, fragile):
    if weight > 50000:
        return [
            [{'fiz': "Макс. вес 50 кг", 'yur': "-", 'item_vat': "-", 'for_declared': "-"}],
            [{'fiz': "Макс. вес 50 кг", 'yur': "-", 'item_vat': "-", 'for_declared': "-"}],
        ]
    return [find_item_cost(zone, weight, declared_value, 'post_office', delivery, notification, fragile),
            find_item_cost(zone, weight, declared_value, 'home',  delivery, notification, fragile)]
