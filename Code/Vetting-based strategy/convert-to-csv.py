# Code to obtain the ratings from excel file and put in csv file

import xlrd
import csv

def csv_from_excel():
    wb = xlrd.open_workbook('annotator-ratings.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open('annotator-ratings-csv.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

# runs the csv_from_excel function:
csv_from_excel()
