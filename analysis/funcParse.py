import re
from pycparser import parse_file, c_ast, c_generator


class CParser:
    def __init__(self, c_file):
        self.c_file = c_file
        self.function_parameters = []
        self.parameters = [] # 存储这个函数的参数
        self.parse_c_file()

    def parse_c_file(self):
        # 读取C文件
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        # 用于匹配函数定义的正则表达式
        function_pattern = r'\b(\w+)\s+(\w+)\s*\((.*?)\)\s*\{'

        # 用于匹配参数的正则表达式
        param_pattern = r'\s*(\w+)\s+(\w+)\s*'

        # 在C代码中查找所有函数定义
        function_matches = re.finditer(function_pattern, c_code)

        # 对于每个函数定义
        for match in function_matches:
            return_type, function_name, params = match.groups()

            # 在参数字符串中查找所有参数
            param_matches = re.findall(param_pattern, params)

            # 存储这个函数的参数
            parameters = [function_name]

            # 对于每个参数
            for param_type, param_name in param_matches:
                # 计算参数在原始代码中的位置
                param_pos = match.start() + match.group().find(param_name)

                # 根据参数的位置计算参数所在的行数
                param_line = c_code.count('\n', 0, param_pos) + 1

                # 将参数添加到列表中
                # parameters.append([self.c_file, param_name, param_line, param_type.upper(), []])
                parameters.append([param_name, param_line, param_type])

            # 将函数参数添加到列表中
            self.parameters.append(parameters)
            self.function_parameters.append({function_name: parameters})

    def get_function_parameters(self):
        return self.function_parameters

    def get_parameters(self):
        return self.parameters



# c_parser = CParser('../test/test.c')
# function_parameters = c_parser.get_function_parameters()
# parameters = c_parser.get_parameters()
# for params in function_parameters:
#     print(params)
# print(parameters)

# # The path to the C file
# c_file = '../test/test.c'
#
# # Read the C file
# with open(c_file, 'r') as f:
#     c_code = f.read()
#
# # The regular expression to match function definitions
# function_pattern = r'\b(\w+)\s+(\w+)\s*\((.*?)\)\s*\{'
#
# # Find all function definitions in the C code
# function_matches = re.findall(function_pattern, c_code)
#
# # A list to store the function parameters
# function_parameters = []
#
# # The regular expression to match parameters
# param_pattern = r'\s*(\w+)\s+(\w+)\s*'
#
# # For each function definition
# for return_type, function_name, params in function_matches:
#     # Find all parameters in the parameters string
#     param_matches = re.findall(param_pattern, params)
#
#     # A list to store the parameters of this function
#     parameters = []
#
#     # For each parameter
#     for param_type, param_name in param_matches:
#         # Add the parameter to the list
#         parameters.append([param_type.upper(), param_name])
#
#     # Add the function parameters to the list
#     function_parameters.append({function_name: parameters})
#
# # Print the function parameters
# for params in function_parameters:
#     print(params)
