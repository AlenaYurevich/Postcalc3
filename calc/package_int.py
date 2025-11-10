
import math
from .sheets import sheet9
from .vat import vat
from .round_as_excel import round_as_excel
from .format import formatted
from .constants import TRACKED_RATE


"""
для мелких пакетов стоимость складывается из стоимости за посылку и стоимости за килограмм
Тарификация  за  массу простого и отслеживаемого мелкого пакет осуществляется с точностью до сотен 
граммов. Любое количество граммов округляется до сотни граммов в большую сторону
"""


def weight(item_weight):
    return math.ceil(item_weight / 100) / 10


def find_numbers_by_country(row_number, priority):
    if row_number < 11:
        # Если номер строки меньше 11, возвращаем None, потому что строки выше 11 не обрабатываются.
        # в файле добавила строку сверху чтобы соответствовало посылкам
        return None
        # Получаем строку по её индексу.
    row_data = list(sheet9.iter_rows(min_row=row_number, max_row=row_number, values_only=True))
    if row_data:  # Проверка, что строка не пустая
        row_data = row_data[0]  # Извлекаем данные строки (поскольку iter_rows возвращает список кортежей)
        if priority == "non_priority":
            data = (row_data[3], row_data[4])  # Получаем данные из 4-й и 5-й колонок
        else:
            data = (row_data[5], row_data[6])  # Получаем данные из 6-й и 7-й колонок
        return data
    # Если row_data пустой или None, возвращаем None, None
    return None


def find_package_int(destination, item_weight, track, priority):
    data = find_numbers_by_country(destination, priority)
    if type(data[0]) is str:
        return {'fiz': "Отправления не принимаются"}
    if track == "tracked":
        add_cost = TRACKED_RATE
    else:
        add_cost = 0
    fiz = (data[0] + data[1] * weight(item_weight) + add_cost) * 1.2
    yur = data[0] + data[1] * weight(item_weight) + add_cost
    item_vat = vat(yur)
    fiz = round_as_excel(fiz)
    yur = round_as_excel(yur) + item_vat
    rate = {
        'fiz': fiz,
        'yur': yur,
        'item_vat': item_vat,
    }
    for key in rate:
        rate[key] = formatted(rate[key])
    return rate


def cost_of_package_int(destination, item_weight):
    print(destination)
    if item_weight > 2000:
        limit_message = "Макс. вес 2 кг"
        limit_result = {'fiz': limit_message, 'yur': "-"}
        return [[limit_result] for _ in range(3)]
    else:
        simple_non_priority = find_package_int(destination, item_weight, "simple", "non_priority")
        simple_priority = find_package_int(destination, item_weight, "simple", "priority")
        tracked_priority = find_package_int(destination, item_weight, "tracked", "priority")
    return [[simple_non_priority],
            [simple_priority],
            [tracked_priority],
            ]
