import xlsxwriter

def writeTwoListsToColumns(filename,titleColumn1,titleColumn2,dataColumn1,dataColumn2):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', titleColumn1)
    worksheet.write('B1', titleColumn2)
    pos = 2
    for d in dataColumn1:
        sq = 'A' + str(pos)
        worksheet.write(sq,d)
        pos = pos+1
    pos = 2
    for d in dataColumn2:
        sq = 'B' + str(pos)
        worksheet.write(sq,d)
        pos += 1
    workbook.close()
