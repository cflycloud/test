import matplotlib.pyplot as plt
import pandas as pd
import pdfkit
import markdown
import seaborn as sns
import os
import datetime
import pytz
# from sklearn.cluster import KMeans
# import plotly.graph_objects as go
# from plottable import Table, ColDef
# import plotly.figure_factory as ff
# from tabulate import tabulate
# from pandas_profiling import ProfileReport
# import imgkit
# from sklearn.preprocessing import LabelEncoder


class CodeAuditReport:
    def __init__(self, token_func, token_val, danger, invalidfunc, invalidval):
        self.token_func_df = pd.DataFrame(token_func, columns=['filepath', 'name', 'line', 'val_type', 'details'])
        self.token_val_df = pd.DataFrame(token_val, columns=['filepath', 'name', 'line', 'val_type', 'details'])
        self.danger_df = pd.DataFrame(danger, columns=['filepath', 'line', 'function_name', 'risk', 'solve'])
        self.invalidfunc_df = pd.DataFrame(invalidfunc, columns=['filepath', 'line', 'name'])
        self.invalidval_df = pd.DataFrame(invalidval, columns=['filepath', 'line', 'name'])

    def open_pdf_with_default_app(self):
        try:
            os.startfile(r"D:\code\CodeAudit\report\output_document\document.pdf")
        except Exception as e:
            print(f"Error occurred while opening the PDF: {e}")

    def generate_report(self):
        current_time = datetime.datetime.now()
        beijing_timezone = pytz.timezone('Asia/Shanghai')
        beijing_time = current_time.astimezone(beijing_timezone)
        beijing_time_str = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

        # markdown文件路径和名称
        content = "# REPORT 代码审计报告\n> 检测时间："
        content += beijing_time_str + "\n\n\n\n\n\n"

        content += "### PART ONE. 变量与函数列表识别输出\n\n"
        content += "#### 1.`token_func`: 识别的函数列表\n"
        content += self.token_func_df.to_markdown(index=False)
        content += "\n\n"
        content += "#### 2.`token_val`: 识别的变量列表\n"
        content += self.token_val_df.to_markdown(index=False)
        content += "\n\n"
        content += "#### 3.`danger`: 识别的风险函数列表\n"
        content += self.danger_df.to_markdown(index=False)
        content += "\n\n"
        content += "#### 4.`invalidfunc`: 识别的无效函数列表\n"
        content += self.invalidfunc_df.to_markdown(index=False)
        content += "\n\n"
        content += "#### 5.`invalidval`: 识别的无效变量列表\n"
        content += self.invalidval_df.to_markdown(index=False)
        content += "\n\n"

        risk_counts = self.danger_df['risk'].value_counts()
        invalid_func_counts = self.invalidfunc_df['name'].value_counts()
        invalid_val_counts = self.invalidval_df['name'].value_counts()

        # 生成报告文件
        md_file = r"D:\code\CodeAudit\report\output_document\document.md"
        css_file = r"D:\code\CodeAudit\report\style\mystyle.css"
        html_file = r"D:\code\CodeAudit\report\output_document\document.html"
        pdf_file = r"D:\code\CodeAudit\report\output_document\document.pdf"
        dir_str = 'D:/code/CodeAudit/report/'

        content += "\n\n\n\n------------------------------\n"
        content += "\n### PATR TWO: PLOT统计绘图\n\n"
        content += "#### 1.BAR 柱状统计图\n\n"
        # 绘制柱状统计图
        if(risk_counts.any()):
            plt.figure(figsize=(10, 6))
            plt.title('Number of each risk')
            sns.barplot(x=risk_counts.index, y=risk_counts.values, alpha=0.8)
            plt.savefig(dir_str + 'images/risk_bar.png')
            content += '''<center>
                              <img src="D:/code/CodeAudit/report/images/risk_bar.png" style="zoom: 70%;" />
                          </center>\n\n'''
        else:
            content += "- 此程序代码中不存在风险函数\n\n"

        if(invalid_func_counts.any()):
            plt.figure(figsize=(10, 6))
            plt.title('Number of each invalid function')
            sns.barplot(x=invalid_func_counts.index, y=invalid_func_counts.values, alpha=0.8)
            plt.savefig(dir_str + 'images/invalid_func_bar.png')
            content += '''<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_func_bar.png" style="zoom: 70%;" />
                          </center>\n\n'''
        else:
            content += "- 此程序代码中不存在无效函数\n\n"

        if(invalid_val_counts.any()):
            plt.figure(figsize=(10, 6))
            plt.title('Number of each invalid variable')
            sns.barplot(x=invalid_val_counts.index, y=invalid_val_counts.values, alpha=0.8)
            plt.savefig(dir_str + 'images/invalid_val_bar.png')
            content += '''<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_val_bar.png" style="zoom: 70%;" />
                          </center>\n\n'''
        else:
            content += "- 此程序代码中不存在无效变量\n\n"

        # 绘制饼图
        content += "#### 2.PIE 饼状统计图\n\n"
        if(risk_counts.any()):
            plt.figure(figsize=(10, 6))
            plt.title('Proportion of each risk')
            plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%')
            plt.savefig(dir_str + 'images/risk_pie.png')
            content += '''<center>
                              <img src="D:/code/CodeAudit/report/images/risk_pie.png" style="zoom: 70%;" />
                          </center>\n\n'''
        else:
            content += "- 此程序代码中不存在风险函数\n\n"

        if(invalid_func_counts.any()):
            plt.figure(figsize=(10, 6))
            plt.title('Proportion of each invalid function')
            plt.pie(invalid_func_counts.values, labels=invalid_func_counts.index, autopct='%1.1f%%')
            plt.savefig(dir_str + 'images/invalid_func_pie.png')
            content += '''<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_func_pie.png" style="zoom: 70%;" />
                          </center>\n\n'''
        else:
            content += "- 此程序代码中不存在无效函数\n\n"

        if(invalid_val_counts.any()):
            plt.figure(figsize=(10, 6))
            plt.title('Proportion of each invalid variable')
            plt.pie(invalid_val_counts.values, labels=invalid_val_counts.index, autopct='%1.1f%%')
            plt.savefig(dir_str + 'images/invalid_val_pie.png')
            content += '''<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_val_bar.png" style="zoom: 70%;" />
                          </center>\n\n'''
        else:
            content += "- 此程序代码中不存在无效变量\n\n"

        # 将markdown内容写入文件
        with open(md_file, 'w', encoding='gb18030', errors='ignore') as f:
          f.write(content)

        # 使用mystyle.css渲染markdown为html
        html = markdown.markdown(open(md_file).read(), extensions=['extra', 'codehilite'])
        html = f'<html><head><link rel="stylesheet" href="{css_file}"></head><body>{html}</body></html>'
        with open(html_file, 'w', encoding='gb18030', errors='ignore') as f:
          f.write(html)

        path_wkthmltopdf = r"D:\\otherAppData\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

        # 将html转换为pdf
        pdfkit.from_file(html_file, pdf_file, configuration=config,
                         options={"enable-local-file-access": "", "encoding": "gb18030"})

        print("报告生成完成。")

# token_func = [
#   ["func1", 10, "void", [["arg1", 10, "int"], ["arg2", 11, "char"]]],
#   ["func2", 30, "int", [["arg1", 30, "int"], ["arg2", 31, "char"], ["arg3", 32, "double"]]],
#   ["func3", 70, "float", [["arg1", 70, "char"], ["arg2", 71, "char"]]],
#   ["func4", 90, "double", [["arg1", 90, "float"], ["arg2", 91, "double"]]],
#   ["func5", 110, "int", [["arg1", 110, "char"], ["arg2", 111, "int"], ["arg3", 112, "int"]]],
#   ["func6", 130, "void", [["arg1", 130, "double"], ["arg2", 131, "char"], ["arg3", 132, "char"]]],
#   ["func7", 150, "float", [["arg1", 150, "int"], ["arg2", 151, "char"]]],
#   ["func8", 170, "int", [["arg1", 170, "int"], ["arg2", 171, "int"], ["arg3", 172, "int"], ["arg4", 173, "char"]]],
#   ["func9", 190, "void", [["arg1", 190, "int"], ["arg2", 191, "double"]]],
#   ["func10", 210, "float", [["arg1", 210, "char"], ["arg2", 211, "double"], ["arg3", 212, "int"]]]
# ]
#
# token_val = [
#   ["var1", 5, "int", [["val1", 5, "int"], ["val2", 6, "int"]]],
#   ["var2", 20, "char", [["val3", 20, "char"], ["val4", 21, "char"]]],
#   ["var3", 50, "double", [["val5", 50, "double"], ["val6", 51, "double"]]],
#   ["var4", 70, "float", [["val7", 70, "float"], ["val8", 71, "float"]]],
#   ["var5", 90, "int", [["val9", 90, "int"], ["val10", 91, "int"]]],
#   ["var6", 110, "char", [["val11", 110, "char"], ["val12", 111, "char"]]],
#   ["var7", 130, "double", [["val13", 130, "double"], ["val14", 131, "double"]]],
#   ["var8", 150, "float", [["val15", 150, "float"], ["val16", 151, "float"]]],
#   ["var9", 170, "int", [["val17", 170, "int"], ["val18", 171, "int"]]],
#   ["var10", 190, "char", [["val19", 190, "char"], ["val20", 191, "char"]]]
# ]
#
# danger = [
#   ["path/to/file1.c", 15, "func1", "Buffer Overflow Risk", "Consider using safer functions such as strncpy"],
#   ["path/to/file2.c", 25, "func2", "Null Pointer Risk", "Check pointer before use"],
#   ["path/to/file3.c", 75, "func3", "Uninitialized Variable Risk", "Initialize variables before use"],
#   ["path/to/file4.c", 35, "func4", "Type Mismatch Risk", "Ensure proper type casting"],
#   ["path/to/file5.c", 45, "func5", "Memory Leak Risk", "Free dynamically allocated memory"],
#   ["path/to/file6.c", 55, "func6", "Division by Zero Risk", "Check denominator before division"],
#   ["path/to/file7.c", 65, "func7", "Array Index Out of Bounds Risk", "Validate array index"],
#   ["path/to/file8.c", 85, "func8", "Infinite Loop Risk", "Add exit condition to the loop"],
#   ["path/to/file9.c", 95, "func9", "Unused Variable Risk", "Remove unused variables"],
#   ["path/to/file10.c", 105, "func10", "File IO Error Risk", "Handle file opening errors"]
# ]
#
# invalidfunc = [
#   ["path/to/file1.c", 16, "func4"],
#   ["path/to/file2.c", 26, "func5"],
#   ["path/to/file3.c", 36, "func6"],
#   ["path/to/file4.c", 46, "func7"],
#   ["path/to/file5.c", 56, "func8"],
#   ["path/to/file6.c", 66, "func9"],
#   ["path/to/file7.c", 76, "func10"],
#   ["path/to/file8.c", 86, "func11"],
#   ["path/to/file9.c", 96, "func12"],
#   ["path/to/file10.c", 106, "func13"]
# ]
#
# invalidval = [
#   ["path/to/file1.c", 7, "var4"],
#   ["path/to/file2.c", 22, "var5"],
#   ["path/to/file3.c", 37, "var6"],
#   ["path/to/file4.c", 52, "var7"],
#   ["path/to/file5.c", 67, "var8"],
#   ["path/to/file6.c", 82, "var9"],
#   ["path/to/file7.c", 97, "var10"],
#   ["path/to/file8.c", 112, "var11"],
#   ["path/to/file9.c", 127, "var12"],
#   ["path/to/file10.c", 142, "var13"]
# ]

# # 将风险转化为数值格式。我们可以使用LabelEncoder对风险进行编码
# encoder = LabelEncoder()
# danger_df['risk_code'] = encoder.fit_transform(danger_df['risk'])

# # KMeans进行聚类
# # 假设我们想要分成3类
# kmeans = KMeans(n_clusters=3)
# danger_df['risk_cluster'] = kmeans.fit_predict(danger_df[['risk_code']])