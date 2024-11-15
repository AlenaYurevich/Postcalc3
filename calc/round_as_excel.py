def round_as_excel(num):
    reminder = str(round(num % 1, 4))+'0000'  # avoid out of index
    # print(reminder, reminder[2], reminder[3], reminder[4], reminder[5])
    if reminder[4] in '6' and reminder[5] in '5':
        return round(num + 0.01, 2)
    elif reminder[3] in '1368' and reminder[4] in '5':
        return round(round(num, 2) + 0.01, 2)
    elif reminder[2] in '025' and reminder[3] in '04' and reminder[4] in '5':
        return round(round(num, 2) + 0.01, 2)
    else:
        return round(num, 2)


"""
def dec(num):
     return Decimal(num).quantize(Decimal("1.00"))  # десятичные числа для отражения денежных средств
decimal не округляет как excel
"""

# print(1, round(0.045, 2))
# print("ожидаю 0,05", round_as_excel(0.045))
# print(2, round(9.3258, 2))
# print("ожидаю 9,33", round_as_excel(9.3258))
# print(3, round(2.235, 2))
# print("ожидаю 2,24", round_as_excel(2.235))
# print(4, round(2.565, 2))
# print("ожидаю 2,57", round_as_excel(2.565))
# print(5, round(2.555, 2))
# print("ожидаю 2,56", round_as_excel(2.555))
# print(6, round(2.505, 2))
# print("ожидаю 2,51", round_as_excel(2.505))
# print(7, round(0.245, 2))
# print("ожидаю 0,25", round_as_excel(0.245))
# print(8, round(17.105, 2))
# print("ожидаю 17.11", round_as_excel(17.105))
# print(9, round(71.815, 2))
# print("ожидаю 71.82", round_as_excel(71.815))
# print(10, round(30.945, 2))
# print("ожидаю 30.95", round_as_excel(30.945))
