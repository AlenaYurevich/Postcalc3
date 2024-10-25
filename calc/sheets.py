import os
from openpyxl import load_workbook


# file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter.xlsx')  # первый файл
# workbook = load_workbook(filename=file_path)
# sheet1 = workbook.active
#
# file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter2.xlsx')  # второй файл
# workbook = load_workbook(filename=file_path)
# sheet2 = workbook.active
#
# file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/parcel_int.xlsx')
# workbook = load_workbook(filename=file_path)
# sheet3 = workbook.active
#
# file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/letter_int.xlsx')
# workbook = load_workbook(filename=file_path)
# sheet4 = workbook.active
#
# file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/ems_points.xlsx')
# wb = load_workbook(filename=file_path)
# sheet5 = wb.active

def load_excel_sheet(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'files/{file_name}')
    workbook = load_workbook(filename=file_path)
    return workbook.active


# Словарь для хранения ссылок на листы
sheets = {
    'letter': load_excel_sheet('letter.xlsx'),
    'letter2': load_excel_sheet('letter2.xlsx'),
    'parcel_int': load_excel_sheet('parcel_int.xlsx'),
    'letter_int': load_excel_sheet('letter_int.xlsx'),
    'ems_points': load_excel_sheet('ems_points.xlsx'),
}

# Доступ к листам через словарь
sheet1 = sheets['letter']
sheet2 = sheets['letter2']
sheet3 = sheets['parcel_int']
sheet4 = sheets['letter_int']
sheet5 = sheets['ems_points']
