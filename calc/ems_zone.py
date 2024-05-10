import os
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/ems_zone.xlsx')
wb = load_workbook(filename=file_path)
sheet = wb.active


def find_ems_zone(worksheet, point1):
    ems_zone = 0
    for row in worksheet.iter_rows(min_row=1, values_only=True):
        if str(row[0]) == point1:
            ems_zone = row[2]
    return ems_zone


print(find_ems_zone(sheet, 'Р13'))
print(get_column_letter(int('P13'[1:]) + 1))

