import tkinter as tk  # 导入tkinter模块，用于创建图形用户界面
from tkinter import ttk, filedialog, messagebox, simpledialog, scrolledtext  # ttk模块:用于创建特殊样式的小部件、filedialog:文件选择框、messagebox确认取消对话框、simpledialog添加文本对话框、scrolledtext:含滚动条的文本框
import shutil

from utils import sortDepartmentNameTxt, listDepartment, addListDepartment, addDepartment, deleteDepartment, updateDepartment
from main import analyze_excel

class DepartmentManagerApp:
    def __init__(self, root):
        """
        创建一个DepartmentManagerApp类，用于管理部门信息

        参数：
        - root: 父窗口对象
        """

        self.data = None  # 添加一个属性来存储导入的Excel文件

        self.root = root
        self.root.title("数据分析统计系统")  # 设置窗口标题

        # 创建一个Treeview
        columns = ('#1')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('#1', text='部门名称')  # 设置列标题

        # 添加 Control + a 全选方法
        def select_all(event):
            self.tree.selection_set(self.tree.get_children())

        self.tree.bind("<Control-a>", select_all)

        # 创建垂直滚动条，command配置滚动条与Treeview关联
        self.tree_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)  
        # 使用yscrollcommand使得滚动条能够根据内容调整长短
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)  

        # 使用grid布局管理Treeview和Scrollbar
        self.tree.grid(row=0, column=1, columnspan=5, rowspan=1, sticky="nsew", pady=(20,0))
        self.tree_scrollbar.grid(row=0, column=6, columnspan=1, sticky="nsw", pady=(20,0))
        
        # root.grid_rowconfigure 行号,伸缩权重,限制最小高度
        self.root.grid_rowconfigure(0,weight=1,minsize=490) 
        self.root.grid_rowconfigure(1,weight=0,minsize=60)
        self.root.grid_rowconfigure(2,weight=1,minsize=60)
        self.root.grid_rowconfigure(3,weight=0,minsize=60)
        # root.grid_columnconfigure 列号,伸缩权重,限制最小宽度
        self.root.grid_columnconfigure(0,weight=1,minsize=100)
        self.root.grid_columnconfigure(1,weight=1,minsize=100)
        self.root.grid_columnconfigure(2,weight=1,minsize=100)
        self.root.grid_columnconfigure(3,weight=1,minsize=100)
        self.root.grid_columnconfigure(4,weight=1,minsize=100)
        self.root.grid_columnconfigure(5,weight=1,minsize=100)
        self.root.grid_columnconfigure(6,weight=1,minsize=100)


        # 创建按钮
        self.import_txt_button = tk.Button(self.root, text="批量导入", command=self.import_department)
        self.import_txt_button.grid(row=1, column=1, columnspan=1, ipadx=20, padx=10, pady=10, sticky="n")

        self.export_txt_button = tk.Button(self.root, text="批量导出", command=self.save_as_file)
        self.export_txt_button.grid(row=1, column=2, columnspan=1, ipadx=20, padx=10, pady=10, sticky="n")

        self.add_txt_button = tk.Button(self.root, text="添加", command=self.add_department)
        self.add_txt_button.grid(row=1, column=3, columnspan=1, ipadx=20, padx=10, pady=10, sticky="n")

        self.delete_txt_button = tk.Button(self.root, text="删除", command=self.delete_department)
        self.delete_txt_button.grid(row=1, column=4, columnspan=1, ipadx=20, padx=10, pady=10, sticky="n")

        self.update_txt_button = tk.Button(self.root, text="修改", command=self.update_department)
        self.update_txt_button.grid(row=1, column=5, columnspan=1, ipadx=20, padx=10, pady=10, sticky="n")

        # 在 row=2 处添加一个文本区域，添加 height 才能不影响其他组件拉伸，且 height 设置的是行数，不能过大，过大还是会影响。
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 14), height=5)
        self.text_area.grid(row=2, column=1, columnspan=5, rowspan=1, padx=(20,0), pady=10, sticky="nsew")

        self.import_excel_button = tk.Button(self.root, text="导入表格", command=self.import_excel)
        self.import_excel_button.grid(row=3, column=1, columnspan=2, ipadx=60, ipady=5, padx=10, pady=(0,20), sticky="n")

        self.export_excel_button = tk.Button(self.root, text="导出表格", command=self.export_excel, state=tk.DISABLED)
        self.export_excel_button.grid(row=3, column=4, columnspan=2, ipadx=60, ipady=5, padx=10, pady=(0,20), sticky="n")

        self.update_prompt("请导入需要转换的 .xls .xlsx .et 格式文件")
        self.load_data()  # 加载数据
        self.center_window()  # 让窗口在屏幕中居中显示


    def load_data(self):
        """
        加载部门列表数据到树形视图控件
        """

        for item in self.tree.get_children():
            self.tree.delete(item)

        department_list = listDepartment()  # 调用listDepartment函数获取部门列表

        for department_name in department_list:
            self.tree.insert('', 'end', values=(department_name,))  # 将部门名称添加到树形视图控件中


    def center_window(self):
        """
        将窗口居中显示在屏幕上
        """
        width = 1000  # 窗口宽度
        height = 750  # 窗口高度

        screen_width = self.root.winfo_screenwidth()  # 获取屏幕宽度
        screen_height = self.root.winfo_screenheight()  # 获取屏幕高度

        x_coordinate = (screen_width - width) // 2  # 计算窗口的 x 坐标
        y_coordinate = (screen_height - height) // 2  # 计算窗口的 y 坐标

        # 设置窗口的初始位置
        self.root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

        # 设置窗口大小不可调整
        # self.root.resizable(False, False)


    def update_prompt(self, new_prompt):
        '''
        更新文本区域
        '''
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)  # 清空文本区域
        self.text_area.insert(tk.END, new_prompt)
        self.text_area.config(state=tk.DISABLED)

    def import_excel(self):
        """
        导入Excel文件
        """
        file_path = filedialog.askopenfilename(title="选择Excel文件", filetypes=[("Excel files", "*.xls;*.xlsx;*.et")])
        
        if file_path:
            try:
                print('导入路径：',file_path)
                self.update_prompt(f"正在处理文件......")
                self.root.update_idletasks()  # 强制刷新界面
                self.data = analyze_excel(file_path)

                if self.data is not None:
                    # print(f'self.data：{self.data}')
                    self.update_prompt(f'处理文件：{file_path}成功！\n请点击"导出表格"按钮选择导出目录')
                    self.export_excel_button['state'] = tk.NORMAL  # 启用导出按钮
                    messagebox.showinfo("成功", f'处理文件成功！请点击"导出表格"按钮选择导出目录')
                else:
                    self.update_prompt(f"self.data为空：{self.data}")
                    self.export_excel_button['state'] = tk.DISABLED  # 禁用导出按钮
                    
            except Exception as e:
                print(f'analyze_excel(file_path)失败,{e}')
                self.update_prompt(f"处理文件：{file_path}失败！\n{e}")
                self.export_excel_button['state'] = tk.DISABLED  # 禁用导出按钮


    def export_excel(self):
        """
        导出Excel文件
        """
        file_path = filedialog.asksaveasfilename(title="保存Excel文件", defaultextension=".xlsx", filetypes=[("Excel files", "*.xls;*.xlsx;*.et")])
        if file_path:
            try:
                print('导出路径：',file_path)
                self.update_prompt(f"正在导出文件......")
                self.root.update_idletasks()  # 强制刷新界面
                self.data.save(file_path)
                self.update_prompt(f"导出文件成功！文件保存在：\n{file_path}")
                messagebox.showinfo("成功", f"导出文件成功！文件保存在：{file_path}")

            except Exception as e:
                print('写入文件失败：', e)


    def import_department(self):
        """
        批量导入部门信息
        """

        # 弹出提示框二次确认
        confirm = messagebox.askyesno("批量导入", "批量导入会导入原本没有的部门（原来部门会保留），确定继续吗？")
        if confirm:
            # 弹出文件选择对话框
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

            if file_path:
                # 读取选择的txt文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    department_list = [line.strip() for line in file.readlines()]

                # 检查并添加部门信息
                result = addListDepartment(department_list)
                if result == 'success':
                    self.load_data()  # 刷新显示数据
                    messagebox.showinfo("成功", "批量导入成功")
                else:
                    messagebox.showerror("错误", result)
        
            sortDepartmentNameTxt()
            self.load_data()


    def save_as_file(self):
        """
        批量导出部门信息
        """

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        # 如果用户取消选择，返回
        if not file_path:
            return

        # 拷贝文件到用户选择的路径
        source_file = './doc/department_name.txt'
        try:
            shutil.copyfile(source_file, file_path)
            self.update_prompt(f"部门列表文件已成功保存到: \n{file_path}")
        except Exception as e:
            self.update_prompt(f"保存文件时出错: \n{e}")


    def add_department(self):
        """
        添加部门信息
        """
        department_name = simpledialog.askstring("添加部门", "请输入部门名称:")  # 弹出对话框，输入部门名称
        if department_name:
            result = addDepartment(department_name)  # 调用addDepartment函数添加部门信息
            if result == 'success':
                self.tree.insert('', 'end', values=(department_name,))  # 将新添加的部门名称添加到树形视图控件中
            else:
                messagebox.showerror("错误", result)  # 弹出错误对话框，显示错误信息
        sortDepartmentNameTxt()
        self.load_data()


    def delete_department(self):
        """
        删除部门信息
        """

        selected_items = self.tree.selection()  # 获取所选中的部门项
        selected_count = len(selected_items)  # 获取选中的部门数量

        if selected_count < 1:
            messagebox.showerror("错误", "请选择至少一个部门进行删除")
            return
        elif selected_count >= 1:
            # 构建确认文本，包含选中的部门数量
            confirm_text = f"确定要删除所选的 {selected_count} 个部门吗？"
            confirm = messagebox.askyesno("确认删除", confirm_text)

            if confirm:
                for selected_item in selected_items:
                    department_name = self.tree.item(selected_item, 'values')[0]  # 获取所选中部门的名称
                    result = deleteDepartment(department_name)  # 调用deleteDepartment函数删除部门信息

                    if result != 'success':
                        messagebox.showerror("错误", result)  # 弹出错误对话框，显示错误信息

                    # 删除树形视图控件中对应的部门信息
                    self.tree.delete(selected_item)

                sortDepartmentNameTxt()
                self.load_data()

    def update_department(self):
        """
        修改部门信息
        """
        selected_item = self.tree.selection()  # 获取所选中的部门名称
        # print('选中数量', len(selected_item))
        if len(selected_item) < 1:
            messagebox.showerror("错误", "请选择一个部门进行修改")  # 弹出错误对话框，显示错误信息
            return
        if len(selected_item) > 1:
            messagebox.showerror("错误", "只能选择一个部门进行修改")  # 弹出错误对话框，显示错误信息
            return

        if selected_item:
            department_name = self.tree.item(selected_item)['values'][0]  # 获取所选中部门的名称
            new_department_name = simpledialog.askstring("修改部门", f"修改{department_name}的部门名称:",initialvalue=department_name)  # 弹出对话框，输入新的部门名称
            if new_department_name:
                result = updateDepartment(department_name, new_department_name)  # 调用updateDepartment函数修改部门信息
                if result == 'success':
                    self.tree.item(selected_item, values=(new_department_name,))  # 修改树形视图控件中对应的部门名称
                    sortDepartmentNameTxt()
                    self.load_data()
                else:
                    messagebox.showerror("错误", result)  # 弹出错误对话框，显示错误信息

if __name__ == "__main__":
    sortDepartmentNameTxt()
    root = tk.Tk()  # 创建一个主窗口对象
    app = DepartmentManagerApp(root)  # 创建一个DepartmentManagerApp对象
    root.mainloop()  # 进入主循环，运行窗口程序
