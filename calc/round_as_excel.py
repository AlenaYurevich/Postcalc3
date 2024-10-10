def round_as_excel(num):
    reminder = str(round(num % 1, 4))+'0000'
    print(reminder, reminder[2], reminder[3])
    if reminder[3] in '02468' and reminder[4] in '5':
        return round(num + 0.01, 2)
    elif reminder[4] in '6' and reminder[5] in '5':
        return round(num + 0.01, 2)
    elif reminder[3] in '02468' and reminder[4] in '5' and reminder[6] in '0123456789':
        return round(num + 0.01, 2)
    else:
        return round(num, 2)


"""
def dec(num):
     return Decimal(num).quantize(Decimal("1.00"))  # десятичные числа для отражения денежных средств
decimal не округляет как excel
"""

print(round(9.3258, 2))
print(round_as_excel(9.3258))
print(3, round(2.235, 2))
print(4, round_as_excel(2.235))
print(5, round(2.565, 2))
print(6, round_as_excel(2.565))
print(round(2.555, 2))
print(round_as_excel(2.555))
print(round(2.505, 2))
print(round_as_excel(2.505))
