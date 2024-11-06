import math
from .sheets import sheet4
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .declared_value import cost_for_declared_value


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
        return math.ceil(item_weight / 100) / 10
    else:
        return math.ceil(item_weight / 10) / 100  # повторяется код с parcel


def find_numbers_by_country(destination, priority):
    # Сопоставление кода назначения с номером строки ячеек
    country_rows = {
        11: (21, 22),  # Австралия
        91: (24, 25),  # Канада
        131: (27, 28),  # Мексика
        164: (30, 31)  # США
    }
    # Получение индексов строк для указанной страны
    start_row, end_row = country_rows.get(destination, (18, 19)) #
    # Определяем столбец в зависимости от приоритета
    column = 'D' if priority == 'non_priority' else 'E'
    # Получаем данные из таблицы
    data = [sheet4[f'{column}{start_row}'].value, sheet4[f'{column}{end_row}'].value]
    return data


def find_package_int_cost(destination, item_weight, declared_value, priority):
    price_row = []
    data = find_numbers_by_country(destination, priority)
    if declared_value in ("нет", "", 0, "0"):
        fiz = data[0] + round_as_excel(data[1] * weight(item_weight, declared_value))
        yur = fiz
        for_declared = ''
    else:
        fiz = 10.90 + data[0] + data[1] * weight(item_weight, declared_value)  # Сбор за объявленную ценность
        fiz = round(fiz, 4)
        for_declared = cost_for_declared_value(declared_value)
        fiz += for_declared
        yur = fiz
        yur = round_as_excel(yur)
        for_declared = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
    item_vat_yur = vat(yur)
    yur = round_as_excel(yur + item_vat_yur)
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat_yur': item_vat_yur,
        'for_declared': for_declared,
        'tracking': "да",
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    price_row.append(rate)
    return price_row


def cost_of_package_int(destination, item_weight, declared_value):
    if item_weight > 2000:
        return [
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
            [{'fiz': "Макс. вес 2 кг", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
        ]
    return [find_package_int_cost(destination, item_weight, declared_value, "non_priority"),
            find_package_int_cost(destination, item_weight, declared_value, "priority")]
