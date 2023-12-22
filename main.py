import pandas as pd
import re

from pypinyin import lazy_pinyin, pinyin, Style
import time

import os
from openpyxl import Workbook
import sys

from utils import sortDepartmentNameTxt, listDepartment


# 时间正则配置文件路径
TIME_REGEX_FILENAME = './doc/time_regex_config.txt'
# 时间正则
time_pattern = '$'

# 其他配置信息文件路径
OTHER_CONFIG_FILENAME = './doc/other_config.txt'
# 单位词
unit_words = []
# 有效数字长度
digital_length = 3
# 其他正则（单位词）
other_pattern = '$'

# 提取编号正则
num_pattern = ''


def generateNumPattern():
    global num_pattern
    num_pattern = f'[a-zA-z]*\d{digital_length,}\b'


# 识别部门名字
def identity_department(abstract: str) -> str:
    departName = ''
    # 1. 拿到 部门表 的所有部门名称集合
    departmentList = listDepartment()

    # 2. 拿到匹配的部门名称
    for thisDepartmentName in departmentList:
        if abstract.startswith(thisDepartmentName):
            # 匹配成功
            departName = thisDepartmentName
            break
    if departName == '':
        print(f'未能识别到部门名称：{abstract}')
    return departName


# 识别姓名
def identity_name(abstract: str) -> str:
    # 1.拿到部门名称
    departmentName = identity_department(abstract)

    # 2.拿到部门名称的长度
    startIndex = len(departmentName)

    # 3.拿到"报销"所在的下标
    endIndex = abstract.find('报销')

    # 如果没有“报销”
    if endIndex == -1:
        result = ''
    else:
        # 4.根据 部门名称的长度 和 "报销"所在的下标 拿到提取的名称
        result = abstract[startIndex:endIndex]
        
    return result


# 读取时间正则配置，构建pattern
def read_time_config():
    global time_pattern
    try:
        with open(TIME_REGEX_FILENAME, 'r', encoding='UTF-8') as file:
            for line in file:
                line = line.strip()  # 去除行末的换行符和空白字符
                time_pattern = time_pattern + "|" + line
    except Exception as e:
        print("读取时间正则配置失败，报错信息：", e)
    print("时间正则：" + time_pattern)


# 读取其他配置信息（单位词、编号中数字部分长度）
def read_other_config():
    global unit_words
    global digital_length
    global other_pattern

    with open(OTHER_CONFIG_FILENAME, 'r', encoding='UTF-8') as file:
        content = file.read()
    lines = content.split('\n')
    for line in lines:
        if line.startswith('单位词：'):
            unit_words = line.replace('单位词：', '').split('、')
        elif line.startswith('编号中数字部分长度：'):
            digital_length = int(line.replace('编号中数字部分长度：', ''))

    # 构建单位词pattern
    for word in unit_words:
        other_pattern = other_pattern + '|' + '\d+' + word
    print('单位词正则：'+other_pattern)
    print('编号中数字部分长度：'+str(digital_length))


# 识别编号
def identity_id(abstract):
    id=''

    # 摘要有报销要提取编号，无报销就不提取编号
    if '报销' not in abstract:
        return id

    abstract = re.sub(time_pattern, '', abstract)  # 把和时间相关的数字给清除
    abstract = re.sub(other_pattern, '', abstract)  # 把和单位词相关的数字清除

    # 构建提取编号的正则
    num_pattern = f'[a-zA-Z]*\\d{{{digital_length},}}'
    matches = re.findall(num_pattern, abstract)
    # id = ''

    # print('我要开始识别编号了')
    # print('num_pattern:'+num_pattern)
    # print("清理后的abstract:"+abstract)
    if len(matches)!=0:
        # 取最后一个编号信息
        id = matches[0]
        # print('识别的编号为：' + id)
    else:
        print(f'未找到匹配的编号：{abstract}')

    return id


# 读取Excel文件
def read_excel(file_path):
    """
    读取Excel文件的函数
    :param file_path: 文件路径
    :return: 二维列表，包含读取到的所有单元格的值
    """
    # 使用pandas读取Excel文件
    df = pd.read_excel(file_path)
    required_columns = ['序号', '摘要', '金额']

    # 检查文件是否包含需要的列
    missing_column = []
    for column in required_columns:
        if column not in df.columns:
            missing_column.append(column)
    if missing_column != []:
        print(f'表格缺少列：{missing_column}')
        raise Exception(f'表格缺少列：{missing_column}')
    
    data = []
    for index, row in df.iterrows():

        num = str(row['序号'])
        abstract = str(row['摘要'])
        money = str(row['金额'])
            
        # 识别 部门名称
        departmentName = identity_department(abstract)
        # 识别编号（摘要中有“报销”，会提取编号，无编号就不会提取编号）
        id = identity_id(abstract)
        # 如果没有识别到部门，则部门列、姓名列都为空
        if departmentName == '':
            name=''
        else:
            # 识别姓名
            name = identity_name(abstract)
        
        # 添加：序号、摘要、金额
        row_data=[]
        row_data.append(int(num))  # 序号
        row_data.append(abstract)  # 摘要
        row_data.append(float(money))  # 金额

        # 添加 部门
        row_data.append(departmentName)
        # 添加 编号
        row_data.append(id)
        # 添加 姓名
        row_data.append(name)

        data.append(row_data)

    print("读取数据完毕！")
    return data


def write_excel(file_extension, data):
    """
    将数据写入Excel文件并按照姓名排序
    :param file_extension: 文件后缀检查
    :param data: 二维列表，包含要写入的数据
    """
    # print(data)
    # 将数据转换为DataFrame对象
    df = pd.DataFrame(data, columns=['序号', '摘要', '金额', '部门', '编号', '姓名'])

    # 添加拼音列
    df['姓名拼音'] = df['姓名'].apply(lambda x: ''.join(pinyin(x, style=Style.NORMAL)[0]) if x else '')

    # 排序
    df = df.sort_values(by=['部门', '编号', '姓名拼音'])

    # 删除姓名拼音列
    df.drop('姓名拼音', axis=1, inplace=True)

    # 根据文件扩展名创建工作簿和工作表
    if file_extension in ['.xlsx', '.xls', '.et']:

        # 将DataFrame转换为列表
        data_list = df.values.tolist()

        # 添加表头
        data_list.insert(0, df.columns.tolist())

        # 创建工作簿wb和工作表ws
        wb = Workbook()
        ws = wb.active

        # 写入数据
        for row in data_list:
            ws.append(row)

        # 保存文件
        # wb.save(file_path)
    else:
        print("不支持的文件格式!系统仅支持xlsx、xls、et格式。")
        raise Exception(f'不支持的文件格式!系统仅支持xlsx、xls、et格式。')

    print("写入数据完毕！")
    return wb


def analyze_excel(input_file):
    # if getattr(sys, 'frozen', False):
    #     main_file_pwd = os.path.dirname(sys.executable)
    # else:
    #     main_file_pwd = os.path.dirname(os.path.abspath(__file__))

    # try:
    #     input_file = sys.argv[1]
    #     print("输入的文件路径：", input_file)

    #     output_file = sys.argv[2]
    #     print("输出的文件路径：", output_file)
    # except Exception as e:
    #     print(f'没有正确传递输入输出路径,e')
    #     raise Exception(f'没有正确传递输入输出路径,e')


    print("开始计时")
    start_time = time.time()  # 记录开始时间

    # 初始化工作
    read_time_config()  # 读取时间正则配置，构建pattern
    read_other_config()  # 读取其他配置信息，读取其他配置信息（单位词、编号中数字部分长度）
    sortDepartmentNameTxt() # 对 department_txt 部门名称进行排序

    try:
        data = read_excel(input_file)
    except Exception as e:
        print(f'read_excel(input_file)失败,{e}')
        raise e

    end_time = time.time()  # 记录结束时间
    read_execution_time = end_time - start_time  # 计算执行时间
    print("读取数据时间：", read_execution_time, "秒")


    # 写入新文件(输出与输入文件在同一文件夹内)
    # 获取输入文件所在目录路径
    # input_dir = os.path.dirname(input_file)
    # print('获取输入文件所在目录路径:'+input_dir)

    # 获取输入文件的扩展名
    file_extension = os.path.splitext(input_file)[1].lower()
    # 输出文件名
    # output_filename = os.path.basename(input_file).split('.')[0] + '_output' + file_extension
    
    try:
        result_excel = write_excel(file_extension, data)
    except Exception as e:
        print(f'写入文件失败：{e}')
        raise Exception(f'写入文件失败：{e}')
    
    end_time = time.time()  # 记录结束时间
    execution_time = end_time - start_time  # 计算执行时间
    print("程序最终执行时间：", execution_time, "秒")
    return result_excel


# def save_excel(result_excel, output_path, output_filename):
#     # 输出文件路径
#     output_path = os.path.join(output_path, output_filename)
#     print('输出文件路径:'+output_path)
#     result_excel.save(output_path)

# try:
#     main()
# except Exception as e:
#     print(e)

# if __name__ == '__main__':
#     main()
