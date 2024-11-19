def read_the_country(worksheet):
    rows = worksheet.max_row
    choices = []
    for i in range(11, rows + 1):
        cell = worksheet.cell(row=i, column=3)
        row = (i, cell.value)
        choices.append(row)
    choices = tuple(choices)
    return choices
