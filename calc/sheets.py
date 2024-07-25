import os
from openpyxl import load_workbook


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')  # первый файл
workbook = load_workbook(filename=file_path)
sheet1 = workbook.active

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
workbook = load_workbook(filename=file_path)
sheet2 = workbook.active
