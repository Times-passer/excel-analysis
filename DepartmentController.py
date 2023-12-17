import os
import sys
import argparse

# 部门信息存放路径
DEPARTMENT_NAME_FILENAME='./doc/department_name.txt'

def addDepartment(departmentName):
    departmentName = str(departmentName).strip()
    departmentList = listDepartment()

    if departmentName in departmentList:
        return 'error：重复添加'

    if departmentName=='' or departmentName=='\n':
        return 'error:添加的部门名称不规范'

    try:
        with open(DEPARTMENT_NAME_FILENAME, 'a',encoding='UTF-8') as file:
            file.write(str(departmentName).strip() + '\n')
    except Exception as e:
        return "error: "+str(e)
    return 'success'

def addListDepartment(departmentNameList : list):
    try:
        with open(DEPARTMENT_NAME_FILENAME, 'w',encoding='UTF-8') as file:
            for thisDepartmentName in departmentNameList:
                if thisDepartmentName and not thisDepartmentName.isspace():
                    file.write(str(thisDepartmentName).strip()+'\n')
    except Exception as e:
        return "error: "+str(e)
    return 'success'


def listDepartment():
    departmentList = []
    try:
        with open(DEPARTMENT_NAME_FILENAME, 'r',encoding='UTF-8') as file:
            for line in file:
                line = line.strip()  # 去除行末的换行符和空白字符
                departmentList.append(line)
    except Exception as e:
        return "error: "+str(e)
    return departmentList

def deleteDepartment(departmentName):
    lines = []

    try:
        with open(DEPARTMENT_NAME_FILENAME, 'r',encoding='UTF-8') as file:
            for line in file:
                if line.strip() != departmentName:
                    lines.append(line)
        with open(DEPARTMENT_NAME_FILENAME, 'w',encoding='UTF-8') as file:
            file.writelines(lines)
    except Exception as e:
        return "error: "+str(e)
    return 'success'




# def main():
    # if getattr(sys, 'frozen', False):
    #     main_file_pwd = os.path.dirname(sys.executable)
    # else:
    #     main_file_pwd = os.path.dirname(os.path.abspath(__file__))
    #
    # # 创建参数解析器
    # parser = argparse.ArgumentParser(description='参数解析器')
    #
    # # 添加命令行选项
    # parser.add_argument('-m', '--method' ,required=True, type=str, choices=['add', 'list', 'delete'], help='执行的方法')
    # parser.add_argument('-n', '--departmentName', nargs='?', help='部门名称')
    #
    # # 解析命令行参数
    # args = parser.parse_args()
    #
    # # 使用参数
    # method = args.method
    # departmentName = args.departmentName
    #
    # # 使用参数
    # # 对参数进行验证和处理
    # if method == 'add':
    #     if departmentName is None:
    #         # print('错误：在添加模式下，名称是必需的。请提供名称参数。')
    #         raise Exception("错误：在添加模式下，部门名称是必需的。请提供部门名称参数。")
    #     else:
    #         # 执行添加操作
    #         result = addDepartment(departmentName)
    #         print(result)
    # elif method == 'delete':
    #     if departmentName is None:
    #         raise Exception("错误：在删除模式下，部门名称是必需的。请提供部门名称参数。")
    #     else:
    #         # 执行添加操作
    #         result = deleteDepartment(departmentName)
    #         print(result)
    # elif method == 'list':
    #     department = listDepartment()
    #     print(department)
    #
    #
    # try:
    #     method = sys.argv[1]
    #     print("执行的方法为：", method)
    # except Exception as e:
    #     print("传递参数错误：", e)
    #
    # if method == 'add':
    #     addResult = addDepartment()
    #     print(addResult)
    #
    # departmentList = listDepartment()
    # print(departmentList)
    #
    # deleteResult = deleteDepartment('八支队（新）')
    # print(deleteResult)

    # list = ['二处',' 三处 ',' ','四处','\n','  ','','五处']
    # addListDepartment(list)
    # department = listDepartment()
    # print(department)
    #
    # add_department_result = addDepartment('\n')
    # print(add_department_result)

# try:
#     main()
# except Exception as e:
#     print(e)

# if __name__ == '__main__':
#     main()