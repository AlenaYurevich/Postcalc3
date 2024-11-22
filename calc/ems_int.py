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
        # Если номер строки меньше 11, возвращаем None, потому что строки выше 11 не обрабатываются.
        return None
        # Получаем строку по её индексу.
    row_data = list(sheet8.iter_rows(min_row=row_number, max_row=row_number, values_only=True))
    if row_data:  # Проверка, что строка не пустая
        row_data = row_data[0]  # Извлекаем данные строки (поскольку iter_rows возвращает список кортежей)
        if item == "documents":
            data = (row_data[3], row_data[4])  # Получаем данные из 3-й и 4-й колонок
        else:
            data = (row_data[5], row_data[6], row_data[7])  # Получаем данные из 5 6 7 колонок
        return data
    # Если row_data пустой или None, возвращаем None, None
    return None


def find_item_cost(destination, weight, declared_value, item):
    price_row = []
    col = find_numbers_by_country(destination, item)
    if type(col[0]) is str:
        return [{'fiz': "отправления не принимаются"}]
    if weight <= 500:
        fiz = col[0]
    elif weight <= 1000:
        fiz = col[1]
    else:
        fiz = col[1] + col[2]
    yur = fiz
    if declared_value in ("нет", "", 0, "0"):
        for_declared = ''
    else:
        for_declared = cost_for_declared_value(declared_value)
        fiz += for_declared
        yur = fiz
        yur = round_as_excel(yur)
        for_declared = round_as_excel(cost_for_declared_value(declared_value)) * 1.2
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


def find_documents_cost(destination, weight, declared_value):
    if weight > 1000:
        return [{'fiz': "Макс. вес 1 кг", 'yur': "-", 'item_vat': "-"}]
    return find_item_cost(destination, weight, declared_value, 'documents')


def find_goods_cost(destination, weight, declared_value):
    if weight > 30000:
        return [{'fiz': "Макс. вес 30 кг", 'yur': "-", 'item_vat': "-"}]
    return find_item_cost(destination, weight, declared_value, 'goods')


print(find_goods_cost(12, 500, 0))
