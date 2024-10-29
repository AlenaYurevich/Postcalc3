import math
from .sheets import sheet3
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .declared_value import cost_for_declared_value


"""
для посылок стоимость складывается из стоимости за посылку и стоимости за килограмм
Тарификация  за  массу  посылки  без  объявленной  ценности  осуществляется  с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
Тарификация  за  массу  посылки с  объявленной  ценностью  осуществляется  с точностью  до  
десятков  граммов.  Любое  количество  граммов  округляется  до  десятков  граммов  в
большую сторону
"""


def weight(item_weight, declared_value):
    if declared_value in ("нет", "", 0, "0"):
        return math.ceil(item_weight / 100) / 10
    else:
        return math.ceil(item_weight / 10) / 100  # повторяется код с parcel


def find_numbers_by_country(row_number, priority):
    if row_number < 11:
        # Если номер строки меньше 11, возвращаем None, потому что строки выше 11 не обрабатываются.
        return None
        # Получаем строку по её индексу.
    row_data = list(sheet3.iter_rows(min_row=row_number, max_row=row_number, values_only=True))
    if row_data:  # Проверка, что строка не пустая
        row_data = row_data[0]  # Извлекаем данные строки (поскольку iter_rows возвращает список кортежей)
        if priority == "non_priority":
            data = (row_data[3], row_data[4])  # Получаем данные из 3-й и 4-й колонок
        else:
            data = (row_data[5], row_data[6])  # Получаем данные из 5-й и 6-й колонок
        return data
    # Если row_data пустой или None, возвращаем None, None
    return None


def find_parcel_int_cost(destination, item_weight, declared_value, priority):
    price_row = []
    col = find_numbers_by_country(destination, priority)
    if type(col[0]) is str:
        return [{'fiz': "Посылки не принимаются"}]
    if declared_value in ("нет", "", 0, "0"):
        fiz = col[0] + round_as_excel(col[1] * weight(item_weight, declared_value))
        yur = fiz
        for_declared_fiz = ''
        for_declared_yur = ''
        sep1 = ''
        sep2 = '/'
    else:
        fiz = 5.85 + col[0] + col[1] * weight(item_weight, declared_value)
        fiz = round(fiz, 4)
        for_declared_fiz = cost_for_declared_value(declared_value)
        fiz += for_declared_fiz
        yur = fiz
        yur = round_as_excel(yur)
        for_declared_yur = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
        sep1, sep2 = "/", "/"
    item_vat_yur = vat(yur)
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


def cost_of_parcel_int(destination, item_weight, declared_value):
    if item_weight > 50000:
        return [
            [{'fiz': "Макс. вес 50 кг", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
            [{'fiz': "Макс. вес 50 кг", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}],
        ]
    return [find_parcel_int_cost(destination, item_weight, declared_value, "non_priority"),
            find_parcel_int_cost(destination, item_weight, declared_value, "priority")]
