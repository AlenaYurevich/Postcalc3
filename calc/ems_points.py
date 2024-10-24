from sheets import sheet5


def read_ems_points(worksheet):
    rows = sheet5.max_row
    choices = []
    for i in range(1, rows + 1):
        cell = worksheet.cell(row=i, column=2)
        row = (i, cell.value)
        choices.append(row)
    choices = tuple(choices)
    return choices


def find_ems_point(worksheet, point):
    ems_point = 0
    for row in worksheet.iter_rows(min_row=1, values_only=True):
        if str(row[0]) == point:
            ems_point = row[2]
    return ems_point


def data_of_ems(departure, destination, item_weight, declared_value):
    zone1 = find_ems_point(sheet5, departure)
    zone2 = find_ems_point(sheet5, destination)
    return [zone1, zone2, item_weight, declared_value]


"""
правильно определяет зоны
"""
