import subprocess
import os
import re

class overflowAnalyzer:
    def __init__(self, c_file):
        self.c_file = c_file
        self.file_name = os.path.splitext(os.path.basename(c_file))[0]
        self.output_dir = os.path.dirname(self.c_file) + '/'
        self.output_exe = self.file_name + '.exe'
        self.dangerList = [] # [[filepath, line, function_name, risk, solve], [filepath, line, function_name, risk, solve].......]
        self.check_array_overflow() # 1.数组溢出检测
        self.check_unsafe_pointer_operations() # 2.检测不安全的指针运算
        self.check_unsafe_pointer_casts() # 3.指针类型转换
        self.check_dynamic_memory_allocations() # 4.动态内存分配
        self.check_stack_overflow() # 5.栈溢出
        self.check_buffer_overflow() # 6.缓冲区溢出
        self.check_data_race() # 7.多线程共享内存：可能导致数据竞争的正则表达式列表
        # self.drmemoryTool() # 8.使用Dr.Memory工具


    # 1.数组溢出检测
    def check_array_overflow(self):
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        array_def_pattern = r'\b(\w+)\s+(\w+)\s*\[\s*(\d+)\s*\]'
        array_access_pattern = r'\b(\w+)\s*\[\s*(\d+)\s*\]'

        array_defs = list(re.finditer(array_def_pattern, c_code))
        array_accesses = list(re.finditer(array_access_pattern, c_code))

        warnings = []

        # 遍历每个数组进行检查
        for array_def in array_defs:
            array_type, array_name, array_size = array_def.groups()
            array_size = int(array_size)
            for array_access in array_accesses:
                access_name, access_index = array_access.groups()
                access_index = int(access_index)
                if access_name == array_name and access_index >= array_size:
                    warning_line = c_code.count('\n', 0, array_access.start()) + 1
                    warnings.append([self.c_file, str(warning_line), '{}[{}]'.format(array_name, access_index), "可能存在数组溢出",
                                     '1. 指定最大接收长度，确保输入不会超过{}数组的大小。\n2. 使用安全的输入函数，如 fgets 函数。fgets 函数可以指定最大接收长度，并且可以防止缓冲区溢出。'.format(array_name)])
                    self.dangerList.append((warnings))
        # print(warnings)
        # return warnings

    # 2.检测不安全的指针运算
    def check_unsafe_pointer_operations(self):
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        unsafe_ptr_op_patterns = [
            r'\b(\w+\s*\*\s*\w+)\s*\+\s*\d+',  # 指针 + 整数
            r'\b(\w+\s*\*\s*\w+)\s*-\s*\d+',  # 指针 - 整数
            r'\b(\w+\s*\*\s*\w+)\s*\[\s*\w+\s*\]',  # 指针[index]
            r'\b\*\s*(\w+\s*\*\s*\w+)',  # *ptr
            r'\b(\w+\s*\*\s*\w+)\s*=\s*NULL',  # ptr = NULL
            r'\bfree\s*\(\s*(\w+\s*\*\s*\w+)\s*\)',  # free(ptr)
            r'\b\(\s*\w+\s*\*\s*\)(\w+\s*\*\s*\w+)',  # (type*)ptr
        ]

        warnings = []
        solve_str = '''确保指针访问的内存区域有效：在进行指针操作之前，确保指针指向的内存区域是有效的并已经分配。可以通过使用合适的内存分配函数（如 malloc、calloc 或 realloc）来分配足够的内存空间，以及在使用指针之前进行必要的空指针检查。
控制指针偏移量：确保对指针的偏移量操作不会越界访问或超出有效的内存范围。在进行指针偏移操作之前，可以使用条件语句或循环来检查偏移量是否在合理范围内，并且不会导致越界访问。
        '''

        # 对每个模式
        for pattern in unsafe_ptr_op_patterns:
            # 在C代码中找到所有不安全的指针操作
            unsafe_ptr_ops = list(re.finditer(pattern, c_code))

            # 检查每个不安全的指针操作
            for match in unsafe_ptr_ops:
                unsafe_ptr_op = match.group()
                warning_line = c_code.count('\n', 0, match.start()) + 1
                warnings.append([self.c_file, str(warning_line), '{}'.format(unsafe_ptr_op), "可能存在不安全的指针操作", solve_str])
                self.dangerList.append(warnings)

        # print(warnings)
        # return warnings

    # 3.指针类型转换
    def check_unsafe_pointer_casts(self):
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        unsafe_ptr_cast_patterns = [
            r'\(\s*char\s*\*\s*\)\s*\w+',  # (char*)variable
            r'\(\s*int\s*\*\s*\)\s*\w+',  # (int*)variable
            r'\(\s*float\s*\*\s*\)\s*\w+',  # (float*)variable
            r'\(\s*double\s*\*\s*\)\s*\w+',  # (double*)variable
            r'\(\s*void\s*\*\s*\)\s*\w+',  # (void*)variable
            r'\(\s*struct\s+\w+\s*\*\s*\)\s*\w+',  # (struct type*)variable
            r'\(\s*union\s+\w+\s*\*\s*\)\s*\w+',  # (union type*)variable
            r'\(\s*enum\s+\w+\s*\*\s*\)\s*\w+',  # (enum type*)variable
            r'\(\s*long\s*\*\s*\)\s*\w+',  # (long*)variable
            r'\(\s*short\s*\*\s*\)\s*\w+',  # (short*)variable
        ]

        warnings = []
        solve_str = "谨慎选择合适的指针类型转换，进行边界检查，避免悬空指针，并使用静态类型检查工具进行检测。同时，使用更安全的替代方案或优化代码逻辑可以减少不安全指针操作的使用。"

        # 对每个模式
        for pattern in unsafe_ptr_cast_patterns:
            # 在C代码中找到所有不安全的指针类型转换
            unsafe_ptr_casts = list(re.finditer(pattern, c_code))

            # 检查每个不安全的指针类型转换
            for match in unsafe_ptr_casts:
                unsafe_ptr_cast = match.group()
                warning_line = c_code.count('\n', 0, match.start()) + 1
                warnings.append([self.c_file, str(warning_line), '{}'.format(unsafe_ptr_cast), "可能存在不安全指针类型转换导致内存溢出风险", solve_str])
                self.dangerList.append(warnings)
        # print(warnings)
        # return warnings

    # 4.动态内存分配
    def check_dynamic_memory_allocations(self):
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        # 动态内存分配的模式
        dynamic_mem_alloc_patterns = [
            r'\bmalloc\s*\(\s*\w+\s*\)',  # malloc(大小)
            r'\bcalloc\s*\(\s*\w+\s*,\s*\w+\s*\)',  # calloc(数量, 大小)
            r'\brealloc\s*\(\s*\w+\s*,\s*\w+\s*\)',  # realloc(指针, 大小)
            r'\bmalloc\s*\(\s*\w+\s*\s+\w+\s*\)',  # malloc(大小 * 数量)
            r'\bcalloc\s*\(\s*\w+\s*\s+\w+\s*,\s*\w+\s*\)',  # calloc(数量 * 大小, 大小)
            r'\brealloc\s*\(\s*\w+\s*\s+\w+\s*,\s*\w+\s*\)',  # realloc(指针 * 大小, 大小)
            r'\bmalloc\s*\(\s*\w+\s*\s+\w+\s*\s+\w+\s*\)',  # malloc(大小 * 数量 * 数量)
            r'\bcalloc\s*\(\s*\w+\s*\s+\w+\s*\s+\w+\s*,\s*\w+\s*\)',  # calloc(数量 * 大小 * 数量, 大小)
            r'\brealloc\s*\(\s*\w+\s*\s+\w+\s*\s+\w+\s*,\s*\w+\s*\)',  # realloc(指针 * 大小 * 数量, 大小)
            r'\bfree\s*\(\s*\w+\s*\)',  # free(指针)
        ]

        warnings = []
        solve_str = "在进行动态内存分配时，根据实际需求合理设置分配的内存大小，避免过度分配。另外，及时释放不再使用的内存，避免内存泄漏。同时，使用内存管理工具进行内存检测和分析，以及编写健壮的代码逻辑来预防内存溢出问题。"

        # 对每个模式
        for pattern in dynamic_mem_alloc_patterns:
            # 在C代码中找到所有的动态内存分配
            dynamic_mem_allocs = list(re.finditer(pattern, c_code))

            # 检查每一个动态内存分配
            for match in dynamic_mem_allocs:
                dynamic_mem_alloc = match.group()
                warning_line = c_code.count('\n', 0, match.start()) + 1
                warnings.append([self.c_file, str(warning_line), '{}'.format(dynamic_mem_alloc), "存在动态内存分配且无限制可能存在内存溢出风险", solve_str])
                self.dangerList.append(warnings)

        # print(warnings)
        # return warnings

    # 5.栈溢出
    def check_stack_overflow(self):
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        # 栈溢出的模式
        stack_overflow_patterns = [
            # (这里是您提供的原始模式列表，已转化为中文注释)
            r'(\b\w+\b)\s*\([^)]*\)\s*\{\s*(?:[^{}]*\{\s*[^{}]*\}\s*)*[^{}]*\b\1\b\s*\([^)]*\)',  # 递归函数
            r'\bchar\s*\w+\s*\[\s*\d{4,}\s*\]',  # 大的局部变量 (字符数组)
            r'(\w+\s*\([^)]*\)\s*;){10,}',  # 大量的函数调用
            r'\bint\s*\w+\s*\[\s*\d{4,}\s*\]',  # 大的局部变量 (整数数组)
            r'\bdouble\s*\w+\s*\[\s*\d{4,}\s*\]',  # 大的局部变量 (双精度浮点数数组)
            r'\bstruct\s+\w+\s*\w+\s*\[\s*\d{4,}\s*\]',  # 大的局部变量 (结构体数组)
            r'\bunion\s+\w+\s*\w+\s*\[\s*\d{4,}\s*\]',  # 大的局部变量 (联合体数组)
            r'\benum\s+\w+\s*\w+\s*\[\s*\d{4,}\s*\]',  # 大的局部变量 (枚举数组)
            r'\blong\s*\w+\s*\[\s*\d{4,}\s*\]',  # 大的局部变量 (长整型数组)
            r'\bshort\s*\w+\s*\[\s*\d{4,}\s*\]'  # 大的局部变量 (短整型数组)
        ]

        warnings = []
        solve_str = "合理设计和使用局部变量，避免在栈上分配过大的数据结构；使用安全的字符串处理函数，确保字符串操作不会越界；避免递归深度过大，使用迭代或其他方式替代递归；使用栈溢出保护机制，如设置栈的最大大小或使用异常处理来捕获溢出情况。"

        # 对每个模式
        for pattern in stack_overflow_patterns:
            # 在C代码中找到所有可能导致栈溢出的原因
            stack_overflow_causes = list(re.finditer(pattern, c_code))

            # 检查每一个可能导致栈溢出的原因
            for match in stack_overflow_causes:
                stack_overflow_cause = match.group()
                warning_line = c_code.count('\n', 0, match.start()) + 1
                warnings.append([self.c_file, str(warning_line), '{}'.format(stack_overflow_cause), "可能存在栈溢出风险", solve_str])
                self.dangerList.append(warnings)
        # print(warnings)
        # return warnings

    # 6.缓冲区溢出
    def check_buffer_overflow(self):
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        # 缓冲区溢出的模式
        buffer_overflow_patterns = [
            # (这里是您提供的原始模式列表，已转化为中文注释)
            r'\bstrcpy\s*\(\s*\w+\s*,\s*\w+\s*\)',  # 无长度检查的strcpy
            r'\bstrcat\s*\(\s*\w+\s*,\s*\w+\s*\)',  # 无长度检查的strcat
            r'\bgets\s*\(\s*\w+\s*\)',  # 无长度检查的gets
            r'\b\w+\s*\[\s*\w+\s*\]\s*=\s*\w+',  # 无边界检查的数组赋值
            r'\b\w+\s*\[\s*\w+\s*\]\s*=\s*".*"',  # 无边界检查的字符串赋值
            r'\bmemcpy\s*\(\s*\w+\s*,\s*\w+\s*,\s*\w+\s*\)',  # 无长度检查的memcpy
            r'\bmemmove\s*\(\s*\w+\s*,\s*\w+\s*,\s*\w+\s*\)',  # 无长度检查的memmove
            r'\bstrncpy\s*\(\s*\w+\s*,\s*\w+\s*,\s*\w+\s*\)',  # 无正确长度检查的strncpy
            r'\bstrncat\s*\(\s*\w+\s*,\s*\w+\s*,\s*\w+\s*\)',  # 无正确长度检查的strncat
            r'\bsprintf\s*\(\s*\w+\s*,\s*".*"\s*,\s*\w+\s*\)'  # 无长度检查的sprintf
        ]

        warnings = []
        solve_str = "使用安全的输入函数，如fgets()代替不安全的输入函数scanf()；对输入进行边界检查，确保输入数据不会超出缓冲区大小；使用字符串截断或拷贝函数，确保字符串长度不会超过目标缓冲区大小；使用安全的内存操作函数，如memcpy()代替不安全的操作函数strcpy()；定期更新和维护系统，以修复已知的缓冲区溢出漏洞。"

        # 对每个模式
        for pattern in buffer_overflow_patterns:
            # 在C代码中找到所有可能导致缓冲区溢出的原因
            buffer_overflow_causes = list(re.finditer(pattern, c_code))

            # 检查每一个可能导致缓冲区溢出的原因
            for match in buffer_overflow_causes:
                buffer_overflow_cause = match.group()
                warning_line = c_code.count('\n', 0, match.start()) + 1
                warnings.append([self.c_file, str(warning_line), '{}'.format(buffer_overflow_cause), "可能存在缓冲区溢出风险", solve_str])

        # print(warnings)
        # return warnings

    # 7.多线程共享内存：可能导致数据竞争的正则表达式列表
    def check_data_race(self):
        with open(self.c_file, 'r') as f:
            c_code = f.read()

        data_race_patterns = [
            r'\bpthread_create\s*\(',  # 创建线程
            r'\bpthread_mutex_lock\s*\(\s*\w+\s*\)',  # 未锁定互斥锁
            r'\bpthread_mutex_unlock\s*\(\s*\w+\s*\)',  # 未解锁互斥锁
            r'\b\w+\s*=\s*\w+\s*;\s*\w+\s*=\s*\w+\s*;'  # 同时操作共享数据
        ]
        warnings = []
        solve_str = "使用互斥锁或信号量对共享内存进行同步访问；使用线程安全的数据结构和操作函数；避免共享可变状态，使用局部变量或线程本地存储；尽量减少对共享内存的写操作，采用只读或只写的方式访问共享数据；合理划分任务和数据，减少线程之间的竞争。"

        # 对每种模式进行遍历搜索
        for pattern in data_race_patterns:
            # 在C代码中找到所有可能导致数据竞争的模式
            data_race_causes_matches = list(re.finditer(pattern, c_code))

            # 检查每个可能导致数据竞争的模式
            for match in data_race_causes_matches:
                data_race_cause = match.group()
                warning_line = c_code.count('\n', 0, match.start()) + 1
                warnings.append([self.c_file, str(warning_line), '{}'.format(data_race_cause), "多线程共享内存，可能存在数据竞争", solve_str])
        # print(warnings)
        # return warnings

    # 9.使用Dr.Memory工具
    def drmemoryTool(self):
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, self.output_exe)
        compile_command = "gcc -o {} {}".format(output_file, self.c_file)

        compile_process = subprocess.run(compile_command, shell=True, check=True)

        if compile_process.returncode == 0:
            drmemory_command = 'drmemory -batch -- ' + self.output_dir + self.file_name
            drmemory_output = subprocess.check_output(drmemory_command, shell=True)
            print(drmemory_output.decode())

    def outputDanger(self):
        print(self.dangerList)
        return self.dangerList




# c_file = 'D:/code/CodeAudit/test/test2.c'
# output_dir = "D:/code/CodeAudit/test/"
# of = overflowAnalyzer(c_file, output_dir)
# of.outputDanger()




