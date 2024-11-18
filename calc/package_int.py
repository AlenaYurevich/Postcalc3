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


def find_numbers_by_country(destination, priority):
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
    data = [sheet4[f'{column}{start_row}'].value, sheet4[f'{column}{end_row}'].value]
    return data


def find_package_int(destination, item_weight, priority):
    data = find_numbers_by_country(destination, priority)
    fiz = data[0] + round_as_excel(data[1] * weight(item_weight, False))
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


def find_package_registered(destination, item_weight, priority, is_registered):
    add_cost = REGISTERED_RATE if is_registered else TRACKED_RATE  # заказной или отслеживаемый мелкий пакет
    data = find_numbers_by_country(destination, priority)
    fiz = data[0] + round_as_excel(data[1] * weight(item_weight, True)) + add_cost
    fiz = round_as_excel(fiz)
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


def cost_of_package_int(destination, item_weight):
    if item_weight > 2000:
        limit_message = "Макс. вес 2 кг"
        return [
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}],
            [{'fiz': limit_message, 'yur': "-"}]
        ]
    else:
        simple_non_priority = find_package_int(destination, item_weight, "non_priority")
        simple_priority = find_package_int(destination, item_weight, "priority")
        tracked_priority = find_package_registered(destination, item_weight, "priority", False)
        registered_non_priority = {'fiz': "Отправления не принимаются"}
        registered_priority = find_package_registered(destination, item_weight, "priority", True)
        if destination == 161:
            registered_non_priority = find_package_registered(destination, item_weight, "non_priority", True)
    return [[simple_non_priority],
            [simple_priority],
            [tracked_priority],
            [registered_non_priority],
            [registered_priority]
            ]
