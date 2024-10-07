def round_as_excel(num):
    reminder = str(round(num % 1, 4))+'0000'
    if reminder[3] in '0' and reminder[4] in '5':
        return round(num + 0.01, 2)
    elif reminder[3] in '02468' and reminder[4] in '5' and reminder[6] in '123456789':
        return round(num + 0.01, 2)
    else:
        return round(num, 2)


"""
def dec(num):
     return Decimal(num).quantize(Decimal("1.00"))  # десятичные числа для отражения денежных средств
decimal не округляет как excel
"""
#
# print(round(9.3258, 2))
# print(round_as_excel(9.3258))
# print(round(2.575, 2))
# print(round_as_excel(2.575))
# print(round(2.565, 2))
# print(round_as_excel(2.565))
# print(round(2.555, 2))
# print(round_as_excel(2.555))
# print(round(2.505, 2))
# print(round_as_excel(2.505))
