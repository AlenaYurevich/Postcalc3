import os
from openpyxl import load_workbook


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/parcel_int.xlsx')
wb = load_workbook(filename=file_path)
sheet = wb.active


def read_the_country(worksheet):
    rows = sheet.max_row
    choices = []
    for i in range(11, rows + 1):
        cell = worksheet.cell(row=i, column=2)
        row = (i, cell.value)
        choices.append(row)
    choices = tuple(choices)
    return choices


# def find_ems_point(worksheet, point):
#     ems_point = 0
#     for row in worksheet.iter_rows(min_row=1, values_only=True):
#         if str(row[0]) == point:
#             ems_point = row[2]
#     return ems_point
#
#
# def data_of_ems(departure, destination, item_weight, declared_value):
#     zone1 = find_ems_point(sheet, departure)
#     zone2 = find_ems_point(sheet, destination)
#     return [zone1, zone2, item_weight, declared_value]
#
