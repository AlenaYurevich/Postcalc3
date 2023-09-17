import math
from openpyxl import load_workbook


filename = 'files/letter.xlsx'
wb = load_workbook(filename, data_only=True)
sheet = wb.active

max_rows = sheet.max_row  # получаем номер последней заполненной строки

for i in range(3, max_rows+1):
    name = sheet.cell(row=i, column=1).value
    rate = sheet.cell(row=i, column=2).value
    if not name:
        continue
    print(name, rate)


def my_letter(weight):
    letter = sheet['B3'].value
    next_20_gram = sheet['B5'].value
    letter_cost = letter + next_20_gram * (math.ceil(weight / 20) - 1)
    return f'Стоимость пересылки письма {letter_cost} руб.\nСтоимость пересылки бандероли {letter_cost} руб.'
