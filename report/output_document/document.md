# REPORT ������Ʊ���
> ���ʱ�䣺2023-07-18 16:42:56





### PART ONE. �����뺯���б�ʶ�����

#### 1.`token_func`: ʶ��ĺ����б�
| filepath                       | name               | line    | val_type   | details                                                                                                             |
|:-------------------------------|:-------------------|:--------|:-----------|:--------------------------------------------------------------------------------------------------------------------|
| D:/code/CodeAudit/test/test.c  | add                | line:6  | int        | [['a', 'line:6', 'int'], ['b', 'line:6', 'int']]                                                                    |
| D:/code/CodeAudit/test/test1.c | add                | line:2  | int        | [['a', 'line:6', 'int'], ['b', 'line:6', 'int']]                                                                    |
| D:/code/CodeAudit/test/test.c  | main               | line:16 | int        | [['main', 'line:18', 'int'], ['s', 'line:20', 'char[10]'], ['str', 'line:21', 'char *'], ['sum', 'line:19', 'int']] |
| D:/code/CodeAudit/test/test2.c | main               | line:11 | int        | [['input', 'line:12', 'char[20]']]                                                                                  |
| D:/code/CodeAudit/test/test.c  | plus               | line:11 | int        | [['c', 'line:11', 'int'], ['d', 'line:11', 'int']]                                                                  |
| D:/code/CodeAudit/test/test2.c | vulnerableFunction | line:5  | void       | [['buffer', 'line:6', 'char[10]']]                                                                                  |

#### 2.`token_val`: ʶ��ı����б�
| filepath                      | name   | line   | val_type   | details   |
|:------------------------------|:-------|:-------|:-----------|:----------|
| D:/code/CodeAudit/test/test.c | a      | line:4 | int        | []        |

#### 3.`danger`: ʶ��ķ��պ����б�
| filepath                       | line    | function_name   | risk             | solve                                                                                                                                                                                           |
|:-------------------------------|:--------|:----------------|:-----------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| D:/code/CodeAudit/test/test.c  | line:20 | char            | ��Σ��           | ���б߽��飬ʹ�����Ƴ��ȵĺ�������ȷ����С���������ܵĳ���                                                                                                                                  |
| D:/code/CodeAudit/test/test.c  | line:23 | scanf           | ��Σ��           | �ܿ��ܱ����⹥����������ĸ�ʽ�ַ���������֤�͹���ȷ���������Ԥ�ڵĸ�ʽ�ͷ�Χ������ʹ��������ʽ����������������֤����������������Ч��.                                                   |
| D:/code/CodeAudit/test/test2.c | line:6  | char            | ��Σ��           | ���б߽��飬ʹ�����Ƴ��ȵĺ�������ȷ����С���������ܵĳ���                                                                                                                                  |
| D:/code/CodeAudit/test/test2.c | line:7  | strcpy          | ��Σ��           | (1)���Ŀ���ַ����ĳ��Ȳ���������Դ�ַ��������ݣ�strcpy �������ᵼ�»�������������������ڴ���������ݡ�������������������ȫ©���������Ϊʹ�� strncpyָ�����Ƶ���󳤶�.                   |
|                                |         |                 |                  | (2)���Ŀ���ַ�����Դ�ַ���ָ����ͬ���ڴ�����strcpy �������޷���ȷ����������δ������Ϊ��ȷ��Ŀ���ַ�����Դ�ַ������ص�������ʹ�� strcpy �İ�ȫ������� strcpy_s���� strncpy_s������������⡣ |
| D:/code/CodeAudit/test/test2.c | line:12 | char            | ��Σ��           | ���б߽��飬ʹ�����Ƴ��ȵĺ�������ȷ����С���������ܵĳ���                                                                                                                                  |
| D:/code/CodeAudit/test/test2.c | line:14 | scanf           | ��Σ��           | �ڸ�ʽ�ַ�����ʹ���޶����������������󳤶ȣ����� '%Ns',��ֹ���������                                                                                                                         |
| D:/code/CodeAudit/test/test.c  | 20      | s[10]           | ���ܴ���������� | 1. ָ�������ճ��ȣ�ȷ�����벻�ᳬ��s����Ĵ�С��                                                                                                                                              |
|                                |         |                 |                  | 2. ʹ�ð�ȫ�����뺯������ fgets ������fgets ��������ָ�������ճ��ȣ����ҿ��Է�ֹ�����������                                                                                                  |

#### 4.`invalidfunc`: ʶ�����Ч�����б�
| filepath                      | line    | name   |
|:------------------------------|:--------|:-------|
| D:/code/CodeAudit/test/test.c | line:11 | plus   |

#### 5.`invalidval`: ʶ�����Ч�����б�
| filepath                      | line    | name   |
|:------------------------------|:--------|:-------|
| D:/code/CodeAudit/test/test.c | line:18 | main   |





------------------------------

### PATR TWO: PLOTͳ�ƻ�ͼ

#### 1.BAR ��״ͳ��ͼ

<center>
                              <img src="D:/code/CodeAudit/report/images/risk_bar.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_func_bar.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_val_bar.png" style="zoom: 70%;" />
                          </center>

#### 2.PIE ��״ͳ��ͼ

<center>
                              <img src="D:/code/CodeAudit/report/images/risk_pie.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_func_pie.png" style="zoom: 70%;" />
                          </center>

<center>
                              <img src="D:/code/CodeAudit/report/images/invalid_val_bar.png" style="zoom: 70%;" />
                          </center>

