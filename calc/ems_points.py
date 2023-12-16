import os
from openpyxl import load_workbook


def read_ems_points():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/ems_points.xlsx')
    wb = load_workbook(filename=file_path)
    sheet = wb.active
    rows = sheet.max_row
    choices = []
    row = ()
    for i in range(2, rows + 1):
        for j in range(1, 3):
            cell = sheet.cell(row=i, column=j)
            row = (i, cell.value)
        choices.append(row)
    choices = tuple(choices)
    return choices


print(read_ems_points())
