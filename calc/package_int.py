import math
from .sheets import sheet4
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .constants import TRACKED_RATE, REGISTERED_RATE


"""
для мелких пакетов стоимость складывается из стоимости за посылку и стоимости за килограмм
Тарификация  за  массу  нерегистрируемых пакетов осуществляется  с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
Тарификация  за  массу  регистрируемых пакетов  осуществляется  с точностью  до  
десятков  граммов.  Любое  количество  граммов  округляется  до  десятков  граммов  в
большую сторону
"""


def weight(item_weight, is_registered):
    if is_registered:
        return math.ceil(item_weight / 10) / 100  # если регистрируемое
    else:
        return math.ceil(item_weight / 100) / 10


def get_rates_from_sheet(destination, priority):
    # Сопоставление кода назначения с номером строки ячеек
    country_rows = {
        11: (21, 22),  # Австралия
        91: (24, 25),  # Канада
        131: (27, 28),  # Мексика
        164: (30, 31)  # США
    }
    # Получение индексов строк для указанной страны
    start_row, end_row = country_rows.get(destination, (18, 19))
    # Определяем столбец в зависимости от приоритета
    column = 'D' if priority == 'non_priority' else 'E'
    # Получаем данные из таблицы
    return [sheet4[f'{column}{start_row}'].value, sheet4[f'{column}{end_row}'].value]


def find_package_int(destination, item_weight, track, priority):
    data = get_rates_from_sheet(destination, priority)
    if track == "registered":
        add_cost = REGISTERED_RATE
    elif track == "tracked":
        add_cost = TRACKED_RATE
    else:
        add_cost = 0
    if track == "simple":
        fiz = round_as_excel(data[0] + data[1] * weight(item_weight, False))
    else:
        fiz = round_as_excel(data[0] + data[1] * weight(item_weight, True)) + add_cost
    item_vat = vat(fiz)
    fiz = round_as_excel(fiz + item_vat)
    yur = fiz
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat': item_vat
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    return rate


def cost_of_package_int(destination, item_weight):
    if item_weight > 2000:
        limit_message = "Макс. вес 2 кг"
        return [{'fiz': limit_message, 'yur': "-"}] * 5
    else:
        simple_non_priority = find_package_int(destination, item_weight, "simple", "non_priority")
        simple_priority = find_package_int(destination, item_weight, "simple", "priority")
        tracked_priority = find_package_int(destination, item_weight, "tracked", "priority")
        registered_non_priority = {'fiz': "Отправления не принимаются"}
        registered_priority = find_package_int(destination, item_weight, "registered", "priority")
        if destination == 161:
            registered_non_priority = find_package_int(destination, item_weight, "registered", "non_priority")
    return [[simple_non_priority],
            [simple_priority],
            [tracked_priority],
            [registered_non_priority],
            [registered_priority]
            ]
