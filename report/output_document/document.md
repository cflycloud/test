# REPORT 代码审计报告
> 检测时间：2023-07-18 16:42:56





### PART ONE. 变量与函数列表识别输出

#### 1.`token_func`: 识别的函数列表
| filepath                       | name               | line    | val_type   | details                                                                                                             |
|:-------------------------------|:-------------------|:--------|:-----------|:--------------------------------------------------------------------------------------------------------------------|
| D:/code/CodeAudit/test/test.c  | add                | line:6  | int        | [['a', 'line:6', 'int'], ['b', 'line:6', 'int']]                                                                    |
| D:/code/CodeAudit/test/test1.c | add                | line:2  | int        | [['a', 'line:6', 'int'], ['b', 'line:6', 'int']]                                                                    |
| D:/code/CodeAudit/test/test.c  | main               | line:16 | int        | [['main', 'line:18', 'int'], ['s', 'line:20', 'char[10]'], ['str', 'line:21', 'char *'], ['sum', 'line:19', 'int']] |
| D:/code/CodeAudit/test/test2.c | main               | line:11 | int        | [['input', 'line:12', 'char[20]']]                                                                                  |
| D:/code/CodeAudit/test/test.c  | plus               | line:11 | int        | [['c', 'line:11', 'int'], ['d', 'line:11', 'int']]                                                                  |
| D:/code/CodeAudit/test/test2.c | vulnerableFunction | line:5  | void       | [['buffer', 'line:6', 'char[10]']]                                                                                  |

#### 2.`token_val`: 识别的变量列表
| filepath                      | name   | line   | val_type   | details   |
|:------------------------------|:-------|:-------|:-----------|:----------|
| D:/code/CodeAudit/test/test.c | a      | line:4 | int        | []        |

#### 3.`danger`: 识别的风险函数列表
| filepath                       | line    | function_name   | risk             | solve                                                                                                                                                                                           |
|:-------------------------------|:--------|:----------------|:-----------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| D:/code/CodeAudit/test/test.c  | line:20 | char            | 低危险           | 进行边界检查，使用限制长度的函数，或确保大小大于最大可能的长度                                                                                                                                  |
| D:/code/CodeAudit/test/test.c  | line:23 | scanf           | 很危险           | 很可能被恶意攻击，对输入的格式字符串进行验证和过滤确保输入符合预期的格式和范围。可以使用正则表达式、条件语句或其他验证机制来检查输入的有效性.                                                   |
| D:/code/CodeAudit/test/test2.c | line:6  | char            | 低危险           | 进行边界检查，使用限制长度的函数，或确保大小大于最大可能的长度                                                                                                                                  |
| D:/code/CodeAudit/test/test2.c | line:7  | strcpy          | 很危险           | (1)如果目标字符串的长度不足以容纳源字符串的内容，strcpy 函数将会导致缓冲区溢出，覆盖其他内存区域的数据。这可能引发程序崩溃或安全漏洞，建议改为使用 strncpy指定复制的最大长度.                   |
|                                |         |                 |                  | (2)如果目标字符串和源字符串指向相同的内存区域，strcpy 函数将无法正确工作，导致未定义行为。确保目标字符串和源字符串不重叠，可以使用 strcpy 的安全替代函数 strcpy_s（或 strncpy_s）来避免此问题。 |
| D:/code/CodeAudit/test/test2.c | line:12 | char            | 低危险           | 进行边界检查，使用限制长度的函数，或确保大小大于最大可能的长度                                                                                                                                  |
| D:/code/CodeAudit/test/test2.c | line:14 | scanf           | 很危险           | 在格式字符串中使用限定符来限制输入的最大长度，例如 '%Ns',防止缓冲区溢出                                                                                                                         |
| D:/code/CodeAudit/test/test.c  | 20      | s[10]           | 可能存在数组溢出 | 1. 指定最大接收长度，确保输入不会超过s数组的大小。                                                                                                                                              |
|                                |         |                 |                  | 2. 使用安全的输入函数，如 fgets 函数。fgets 函数可以指定最大接收长度，并且可以防止缓冲区溢出。                                                                                                  |

#### 4.`invalidfunc`: 识别的无效函数列表
| filepath                      | line    | name   |
|:------------------------------|:--------|:-------|
| D:/code/CodeAudit/test/test.c | line:11 | plus   |

#### 5.`invalidval`: 识别的无效变量列表
| filepath                      | line    | name   |
|:------------------------------|:--------|:-------|
| D:/code/CodeAudit/test/test.c | line:18 | main   |





------------------------------

### PATR TWO: PLOT统计绘图

#### 1.BAR 柱状统计图

<center>
                              <img src="D:/code/CodeAudit/report/images/risk_bar.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_func_bar.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_val_bar.png" style="zoom: 70%;" />
                          </center>

#### 2.PIE 饼状统计图

<center>
                              <img src="D:/code/CodeAudit/report/images/risk_pie.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_func_pie.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_val_bar.png" style="zoom: 70%;" />
                          </center>

