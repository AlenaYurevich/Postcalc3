from .sheets import sheet7
from .format import formatted


def get_values_and_vat(sheet, start_row, end_row):
    """Функция для получения значений и вычисления НДС."""
    values = [sheet[f'F{i}'].value for i in range(start_row, end_row + 1)]
    vat_values = [(value / 120 * 20) for value in values]
    return values, vat_values


def cost_of_sml():
    # Получаем значения и НДС
    values, vat_values = get_values_and_vat(sheet7, 5, 7)
    parcel_values, parcel_vat_values = get_values_and_vat(sheet7, 9, 11)

    # Создаем пустой словарь для хранения всех данных
    rate = {}
    # Добавляем параметры писем и НДС
    for i in range(3):
        rate[f'fiz{i + 1}'] = values[i]  # Например, 'fiz1': значение из ячейки F5
        rate[f'item_vat{i + 1}'] = vat_values[i]  # Например, 'item_vat1': НДС для значения из ячейки F5

    # Добавляем параметры для посылок и соответствующие им НДС
    for i in range(3):
        rate[f'parcel_fiz{i + 1}'] = parcel_values[i]  # Например, 'parcel_fiz1': значение из ячейки F9
        rate[f'parcel_item_vat{i + 1}'] = parcel_vat_values[i]  # Например, 'parcel_item_vat1': НДС для ячейки F9

    rate['tracking'] = "да"

    # Форматируем значения при помощи formatted и добавляем в список
    formatted_rate = {key: formatted(value) for key, value in rate.items()}

    # Возвращаем список с отформатированными данными
    return [formatted_rate]
