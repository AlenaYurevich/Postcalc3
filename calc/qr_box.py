from .sheets import sheet2
from .round_as_excel import round_as_excel
from .format import formatted
from .vat import vat
from .constants import notification_cost


def cost_of_qr_box(declared_value, notification):
    notification = notification_cost(notification)
    fiz = sheet2['D54'].value
    yur = sheet2['H42'].value
    for_declared_fiz, for_declared_yur = " ", " "
    sep1, sep2 = "", ""
    if declared_value not in ("нет", "", 0, "0"):
        for_declared_fiz = round_as_excel(float(declared_value) * 0.01)
        if for_declared_fiz < 0.50:
            for_declared_fiz = 0.50
        for_declared_yur = for_declared_fiz
        fiz += for_declared_fiz
        yur += for_declared_yur
        for_declared_yur = for_declared_fiz * 1.2
        sep1, sep2 = "/", "/"
    if notification == 0.45:
        fiz += notification * 1.2
        yur += notification
        notification = notification * 1.2
    else:
        notification = ""
    item_vat_yur = round_as_excel(vat(yur))
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
        'sep2': "/",
        'notification': notification,
    }
    for i in rate:
        rate[i] = formatted(rate[i])
    for i in rate:
        rate[i] = formatted(rate[i])
    return rate


def cost_of_parcel_qr(item_weight, declared_value, notification):
    price_row = []
    if item_weight <= 25000:
        rate = cost_of_qr_box(declared_value, notification)
        price_row.append(rate)
    else:
        fiz = "Макс. вес ограничен размерами ячейки"
        sep = ''
        price_row.append({'fiz': fiz, 'sep': sep})
    return price_row
