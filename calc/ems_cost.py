import os
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
# from .ems_zone import find_ems_zone


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/ems_rates.xlsx')
wb = load_workbook(filename=file_path)
sheet = wb.active


def find_ems_cost(point1, point2):
    x = get_column_letter(point1)
    y = str(int(point2))
    return sheet[str(x + y)].value


def find_column_letter(zone):
    letters = ' DEFGH'  # name of columns correspond to tariff zones 1-5
    return letters[zone]


for i in range(1, 6):
    print(find_column_letter(i))


print(find_ems_cost(5, 10))
