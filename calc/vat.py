from .round_as_excel import round_as_excel


def vat(num):
    return round_as_excel(num * 0.2)  # расчет НДС 20 %
