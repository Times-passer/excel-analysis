# 部门信息存放路径
DEPARTMENT_NAME_FILEPATH='./doc/department_name.txt'

def sortDepartmentNameTxt():
        
    '''
    对 department_txt 进行格式化。
    为了解决:如果同时存在八支队、八支队(新),而Excel表中的某行支队名称为“八支队(新)”,导出来的Excel显示部门名称为“八支队”的问题,需要把长度更长的放在前面。
    '''

    try:
        with open(DEPARTMENT_NAME_FILEPATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # 去重
        seen_lines = set()  # 用集合来记录已经出现过的行
        unique_lines = []   # 用列表来存储、写回不重复的行，不用集合记录是因为集合会乱序

        for line in lines:
            stripped_line = line.strip()
            if stripped_line not in seen_lines:
                seen_lines.add(stripped_line)
                unique_lines.append(line)

        with open(DEPARTMENT_NAME_FILEPATH, 'w', encoding='utf-8') as f:
            # 排序，按字符串长度降序排序并保留原顺序
            sorted_lines = sorted(unique_lines, key=lambda x: len(x), reverse=True)
            # 去空格
            f.writelines(line for line in sorted_lines if line.strip())

    except Exception as e:
        print(f"department_txt格式化失败: {e}", )
    
    print('department_txt格式化成功')


def listDepartment():
    '''
    查
    '''

    departmentList = []
    try:
        with open(DEPARTMENT_NAME_FILEPATH, 'r',encoding='UTF-8') as file:
            for line in file:
                line = line.strip()  # 去除行末的换行符和空白字符
                departmentList.append(line)
    except Exception as e:
        return f"error: {e}"
    
    return departmentList


def addListDepartment(departmentNameList : list):
    '''
    批量增
    '''

    try:
        with open(DEPARTMENT_NAME_FILEPATH, 'w',encoding='UTF-8') as file:
            for thisDepartmentName in departmentNameList:
                if thisDepartmentName and not thisDepartmentName.isspace():
                    file.write(str(thisDepartmentName).strip()+'\n')
    except Exception as e:
        return f"error: {e}"
    
    return 'success'


def addDepartment(departmentName):
    '''
    增
    '''

    # 检查新部门名称是否已经存在
    if departmentName in listDepartment():
        return 'error: 重复添加'
    
    departmentName = str(departmentName).strip()
    if departmentName=='' or departmentName=='\n':
        return 'error: 添加的部门名称不规范'

    try:
        with open(DEPARTMENT_NAME_FILEPATH, 'a',encoding='UTF-8') as file:
            file.write(str(departmentName).strip() + '\n')
    except Exception as e:
        return f"error: {e}"
    
    return 'success'


def deleteDepartment(departmentName):
    '''
    删
    '''

    try:
        with open(DEPARTMENT_NAME_FILEPATH, 'r', encoding='UTF-8') as file:
            lines = file.readlines()

        # 使用临时列表来存储修改的内容
        modified_lines = []

        deleted = False
        for line in lines:
            if line.strip() != str(departmentName).strip():
                modified_lines.append(line)
            else:
                deleted = True

        if not deleted:
            return f"error: 部门 {departmentName} 不存在"

        # 将修改的内容写回到文件中
        with open(DEPARTMENT_NAME_FILEPATH, 'w', encoding='UTF-8') as file:
            file.writelines(modified_lines)

    except Exception as e:
        return f"error: {e}"

    return 'success'


def updateDepartment(oldDepartmentName,newDepartmentName):
    '''
    改
    '''

    # 检查新部门名称是否已经存在
    if newDepartmentName in listDepartment():
        return "error: 部门已存在"
    
    oldDepartmentName = str(oldDepartmentName).strip()
    newDepartmentName = str(newDepartmentName).strip()
    #标识符： 是否存在oldDepartmentName
    isExist = False
    try:
        with open(DEPARTMENT_NAME_FILEPATH, 'r',encoding='UTF-8') as file:
            for line in file:
                line = line.strip()  # 去除行末的换行符和空白字符
                if oldDepartmentName==line:
                    isExist = True
                    break
        if isExist==True:
            deleteDepartment(oldDepartmentName)
            addDepartment(newDepartmentName)
        else:
            return "error: "+"部门不存在"
    except Exception as e:
        return f"error: {e}"

    return 'success'
