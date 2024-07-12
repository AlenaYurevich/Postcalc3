from round_as_excel import round_as_excel
from format import formatted


def amount_match(amount):
    if amount > 500:
        return 0.5
    elif amount > 300:
        return 1
    elif amount > 150:
        return 2
    else:
        return 3


def find_transfer_cost(amount):
    price_row = []
    rate = {
        'fiz': 1.00,
        'yur': 1.20,
            }
    multiplier = amount_match(amount)
    fiz = round_as_excel(amount * multiplier / 100)
    yur = fiz * 1.2
    if fiz >= 1.00:
        rate = {
            'fiz': fiz,
            'yur': yur,
                }
    for i in rate:
        rate[i] = formatted(rate[i])
    price_row.append(rate)
    return price_row


print(find_transfer_cost(1000))
