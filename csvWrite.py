import xlsxwriter
from string import ascii_uppercase

def write(data,filename):
    workbook = xlsxwriter.Workbook(filename+'.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.set_column(1, 1, 40)
    worksheet.set_column(2, 2, 20)

    i = 1
    for row in data:
        j = 0
        for column in row:
            position = ascii_uppercase[j] + str(i)
            worksheet.write(position, column)
            j += 1
        i += 1

    workbook.close()
