import math
from .sheets import sheet8
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .declared_value import cost_for_declared_value


"""
для EMS стоимость складывается из стоимости за отправление и стоимости за килограмм
Тарификация  за  массу  EMS  без  объявленной  ценности  осуществляется  с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
Тарификация  за  массу  посылки с  объявленной  ценностью  осуществляется  с точностью  до  
десятков  граммов.  Любое  количество  граммов  округляется  до  десятков  граммов  в
большую сторону
"""


def find_numbers_by_country(row_number, item):
    if row_number < 10:
        # Если номер строки меньше 11 возвращаем None, потому что строки выше 11 не обрабатываются.
        return None
        # Получаем строку по её индексу.
    row_data = list(sheet8.iter_rows(min_row=row_number, max_row=row_number, values_only=True))
    if row_data:  # Проверка, что строка не пустая
        row_data = row_data[0]  # Извлекаем данные строки (поскольку iter_rows возвращает список кортежей)
        if item == "documents":
            data = (row_data[3], row_data[4], row_data[7], row_data[8])  # Получаем данные из 3-й 4-й и 7 колонок
        else:
            data = (row_data[5], row_data[6], row_data[7], row_data[8])  # Получаем данные из 5 6 7 колонок
        return data
    # Если row_data пустой или None, возвращаем None, None
    return None


def ems_weight(weight):
    return math.ceil((weight - 1000) / 1000)


def find_item_cost(destination, weight, declared_value, item):
    price_row = []
    col = find_numbers_by_country(destination, item)
    if type(col[0]) is str:
        return [{'fiz': "отправления не принимаются"}]
    if weight <= col[3] * 1000:
        fiz = col[1] + ems_weight(weight) * col[2]
    elif weight <= 1000:
        fiz = col[1]
    elif weight <= 500:
        fiz = col[0]
    else:
        fiz = 0
    if declared_value in ("нет", "", 0, "0"):
        for_declared = ''
    else:
        for_declared = cost_for_declared_value(declared_value)
        fiz += for_declared
        for_declared = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
    yur = fiz
    yur = round_as_excel(yur)
    item_vat_yur = vat(yur)
    fiz = round_as_excel(fiz + item_vat_yur)
    yur = fiz
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat': item_vat_yur,
        'for_declared': for_declared
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    price_row.append(rate)
    return price_row


def cost_of_ems_int(destination, weight, declared_value):
    max_weight = find_numbers_by_country(destination, 'documents')[3]
    if weight > max_weight * 1000:
        return [
            [{'fiz': f"Макс. вес {max_weight} кг", 'yur': "-", 'item_vat': "-"}],
            [{'fiz': f"Макс. вес {max_weight} кг", 'yur': "-", 'item_vat': "-"}],
        ]
    return [find_item_cost(destination, weight, declared_value, 'documents'),
            find_item_cost(destination, weight, declared_value, 'goods')]
