import os
from openpyxl import load_workbook


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/ems_points.xlsx')
wb = load_workbook(filename=file_path)
sheet = wb.active


def read_ems_points(worksheet):
    rows = sheet.max_row
    choices = []
    for i in range(1, rows + 1):
        cell1 = worksheet.cell(row=i, column=2)
        row = (i, cell1.value)
        choices.append(row)
    choices = tuple(choices)
    return choices


def find_ems_zone(worksheet, departure):
    # zone_list = []
    departure_point = 0
    for row in worksheet.iter_rows(min_row=1, values_only=True):
        # zone_list.append(row)
        if str(row[0]) == departure:
            departure_point = row[2]
    return departure_point


def cost_of_ems(departure, item_weight, declared_value):
    zone1 = find_ems_zone(sheet, departure)
    return departure, zone1, item_weight, declared_value


print(read_ems_points(sheet))
print(find_ems_zone(sheet, 5))
print(cost_of_ems(1, 200, 10))
"""
правильно определяет зоны
"""
