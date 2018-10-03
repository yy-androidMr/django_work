# coding:utf-8
# import xlrd, xlwt
#
# pageRecorders = 5  # 每页数据条数
# fileName = 'cccc.xlsx'  # 目标文件名
# newFileName = '123'  # 新文件名
# newFileNameType = '.xls'
# newSheetName = 'page'  # 新建的sheet名字，如:page1
# sheetNum = 0  # 所取数据在第几个sheet，如在第一个则为0
#
# page = 0  # 页码
# data = xlrd.open_workbook(fileName)  # 打开demo.xls
# data.sheet_names()  # 获取xls文件中所有sheet的名称
# table = data.sheet_by_index(sheetNum)  # 通过索引获取xls文件第0个sheet
# # 获取行数和列数
# nrows = table.nrows
# ncols = table.ncols
#
# for i in range(nrows):
#     if i % pageRecorders == 0:
#         page = page + 1
#     newFile = xlwt.Workbook()  # 写xls文件
#     newTable = newFile.add_sheet(newSheetName + str(page))
#     for j, l in enumerate(table.row_values(i)):
#         newTable.write(i % pageRecorders, j, l)
# newFile.save(newFileName + str(page) + newFileNameType)
# import  docx
# if __name__ == '__main__':
#     file = docx.Document(r"I:\largue_of_memory\ere\一些文件\心 - 副本.doc")
#     print("段落数:" + str(len(file.paragraphs)))
#     # a = 1 << 2
#     # print(36/32)

# def deco2(func):
#     def wrapper():
#         start_time = time.time()
#         func()
#         print('time2:%d' % start_time)
#
#     return wrapper
#
#
# def deco(func):
#     def wrapper():
#         start_time = time.time()
#         func()
#         print('time1:%d' % start_time)
#
#     return wrapper
#
#
# @deco2
# @deco
# def fun():
#     print('hello')
#
#
# fun()


# import sys
# print(sys.path)


# print("请输入娄敏慧的年龄:")
# while True:
#     a = input()
#     age = int(a)
#     if age == 18:
#         print("猜对了")
#         break
#     else:
#         if age > 18:
#             print("不对,她没那么大")
#         else:
#             print("不是的,她没那么小")
#
# print("那你说,她漂不漂亮?")
# while True:
#     b = input()
#     content = str(b)
#     if '不' in content or  '漂亮' not in content:
#         print('别乱说,小心你的嘴')
#     else:
#         print('嗯.小年轻还算识相.')
#
# class fieldTest:
#     field1 = 'f1'
#     f2 = 'f2222'
#     f3 = 'f333'
#
#     def __init__(self):
#         self.a = 1
#
#
# f_ins = fieldTest()
# # for i,j in vars(f_ins).items(f_ins):
# #     print(i)
# # print(hasattr(f_ins,'__getattribute__'))
# # print(f_ins.__getattribute__('f2'))
# print(f_ins.__dict__)
# print(fieldTest.__dict__)
# print(f_ins.__dir__())
# print(f_ins.__dir__())
# print([getattr(f_ins, attr) for attr in dir(f_ins)])
# print(vars(if_ins))
# print([f.name for f in f_ins.fields])

