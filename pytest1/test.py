# coding:utf-8
import xlrd, xlwt

pageRecorders = 5  # 每页数据条数
fileName = 'cccc.xlsx'  # 目标文件名
newFileName = '123'  # 新文件名
newFileNameType = '.xls'
newSheetName = 'page'  # 新建的sheet名字，如:page1
sheetNum = 0  # 所取数据在第几个sheet，如在第一个则为0

page = 0  # 页码
data = xlrd.open_workbook(fileName)  # 打开demo.xls
data.sheet_names()  # 获取xls文件中所有sheet的名称
table = data.sheet_by_index(sheetNum)  # 通过索引获取xls文件第0个sheet
# 获取行数和列数
nrows = table.nrows
ncols = table.ncols

for i in range(nrows):
    if i % pageRecorders == 0:
        page = page + 1
    newFile = xlwt.Workbook()  # 写xls文件
    newTable = newFile.add_sheet(newSheetName + str(page))
    for j, l in enumerate(table.row_values(i)):
        newTable.write(i % pageRecorders, j, l)
newFile.save(newFileName + str(page) + newFileNameType)

