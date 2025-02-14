from .round_as_excel import round_as_excel
from .format import formatted
from .vat import vat


def amount_match(amount):
    if amount > 500:
        return 0.5
    elif amount > 300:
        return 1
    elif amount > 150:
        return 2
    else:
        return 3


def cost_of_internal_transfer(amount):
    price_row = []
    rate = {
        'fiz': 1.00,
        'yur': 1.20,
        'fiz_home': 1.35,
            }
    multiplier = amount_match(amount)
    fiz = round_as_excel(amount * multiplier / 100)
    item_vat = round_as_excel(vat(fiz))
    yur = fiz + item_vat
    fiz_home = fiz + 0.35
    if fiz >= 1.00:
        rate = {
            'fiz': fiz,
            'yur': yur,
            'item_vat': item_vat,
            'fiz_home': fiz_home,
                }
    for i in rate:
        rate[i] = formatted(rate[i])
    rate['yur_home'] = "нет"
    price_row.append(rate)
    return price_row
