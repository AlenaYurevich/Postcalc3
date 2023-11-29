def round_as_excel(num):
    num = float(num)
    reminder = str(round(num % 1, 3))
    if reminder[3] in '02468' and reminder[4] in '56789':
        return round(num + 0.01, 2)
    else:
        return round(num, 2)

#
# print(round_as_excel(2.504))
# print(round_as_excel(2.5065))
# print(round_as_excel(2.515))
# print(round_as_excel(2.525))
# print(round_as_excel(2.535))
# print(round_as_excel(2.545))
# print(round_as_excel(2.555))
