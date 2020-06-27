from data import data
import xlsxwriter as x

def initialize(data):
    workbook = x.Workbook("data.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write("A1", "Video Title")
    worksheet.write("B1", "Uploader")
    worksheet.write("C1", "Image URL")

    for i, entry in enumerate(data):
        month = entry[0]
        worksheet.write(0, i + 3, month)

    return (workbook, worksheet)

def insert_month(workbook, worksheet, top10, dic, row, col):
    for video in top10:
        title, uploader, dislikes = video[0], video[1], video[2]
        if title not in dic:
            dic[title] = row # saves what row a video occupies
            row += 1
            worksheet.write(row, 0, title)
            worksheet.write(row, 1, uploader)
        worksheet.write(dic[title] + 1, col, float(dislikes) * 1000000) # converts from millions

    col += 1
    return (workbook, dic, row, col)

dic = {}
row = 0
col = 3
data = data()
(workbook, worksheet) = initialize(data)

for i in range(len(data)):
    (workbook, dic, row, col) = insert_month(workbook, worksheet, data[i][1], dic, row, col)

workbook.close()