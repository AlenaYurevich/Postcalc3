def round_as_excel(num):
    # num = float(num)
    reminder = str(round(num % 1, 3))+'0000'
    if reminder[3] in '02468' and reminder[4] in '56789':
        return round(num + 0.01, 2)
    else:
        return round(num, 2)
