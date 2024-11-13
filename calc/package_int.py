import math
from .sheets import sheet4
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .declared_value import cost_for_declared_value
from .constants import TRACKED_RATE, REGISTERED_RATE, VALUE_RATE


"""
для мелких пакетов стоимость складывается из стоимости за посылку и стоимости за килограмм
Тарификация  за  массу  нерегистрируемых пакетов осуществляется  с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
Тарификация  за  массу  регистрируемых пакетов  осуществляется  с точностью  до  
десятков  граммов.  Любое  количество  граммов  округляется  до  десятков  граммов  в
большую сторону
"""


def weight(item_weight, declared_value):
    if declared_value in ("нет", "", 0, "0"):
        return math.ceil(item_weight / 100) / 10
    else:
        return math.ceil(item_weight / 10) / 100  # если есть объявленная ценность


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


def find_package_int(destination, item_weight, declared_value, priority):
    data = find_numbers_by_country(destination, priority)
    if declared_value in ("нет", "", 0, "0"):
        fiz = data[0] + round_as_excel(data[1] * weight(item_weight, declared_value))
        for_declared = ''
        print("без НДС", (round_as_excel(data[1] * weight(item_weight, declared_value))))
        print("вес1", weight(item_weight, declared_value))
        print("физ1", fiz)
    else:
        fiz = VALUE_RATE + data[0] + data[1] * weight(item_weight, declared_value)  # Сбор за объявленную ценность
        fiz = round(fiz, 4)
        for_declared = cost_for_declared_value(declared_value)
        fiz += for_declared
        fiz = round_as_excel(fiz)
        for_declared = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
    item_vat = vat(fiz)
    fiz = round_as_excel(fiz + item_vat)
    yur = fiz
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat': item_vat,
        'for_declared': for_declared,
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    return rate


def find_package_registered(destination, item_weight, priority, is_registered):
    add_cost = REGISTERED_RATE if is_registered else TRACKED_RATE  # заказной или отслеживаемый мелкий пакет
    data = find_numbers_by_country(destination, priority)
    fiz = data[0] + round_as_excel(data[1] * weight(item_weight, 10)) + add_cost
    print("вес", weight(item_weight, 10))
    print("физ без округления", data[0] + data[1] * weight(item_weight, 10) + add_cost)
    fiz = round_as_excel(fiz)
    print("физ", fiz)
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


def cost_of_package_int(destination, item_weight, declared_value):
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
        simple_non_priority = find_package_int(destination, item_weight, 0, "non_priority")
        simple_priority = find_package_int(destination, item_weight, 0, "priority")
        tracked_priority = find_package_registered(destination, item_weight, "priority", False)
        registered_non_priority = {'fiz': "Отправления не принимаются"}
        registered_priority = find_package_registered(destination, item_weight, "priority", True)
        declared_non_priority = {'fiz': "-", 'yur': "-"}
        declared_priority = {'fiz': "-", 'yur': "-"}
    if declared_value not in ("", "0"):
        declared_priority = find_package_int(destination, item_weight, declared_value, "priority")
        if destination == 161:
            registered_non_priority = find_package_registered(destination, item_weight, "non_priority", True)
            declared_non_priority = find_package_int(destination, item_weight, declared_value, "non_priority")
        else:
            registered_non_priority = {'fiz': "Отправления не принимаются"}
            declared_non_priority = {'fiz': "Отправления не принимаются"}
    else:
        if destination == 161:
            registered_non_priority = find_package_registered(destination, item_weight, "non_priority", True)
    return [[simple_non_priority],
            [simple_priority],
            [tracked_priority],
            [registered_non_priority],
            [registered_priority],
            [declared_non_priority],
            [declared_priority]
            ]
