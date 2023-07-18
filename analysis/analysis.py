import os.path
import re
from PyQt5 import QtCore
import pymysql
from analysis.funcParse import CParser
from analysis.find_danger import Danger
from analysis.overflow import overflowAnalyzer
# from find_danger import Danger

class Function:
    def __init__(self, filepath='', name='', val_type='', type="", line=""):
        self.filepath = filepath
        self.name = name
        self.val_type = val_type
        self.type = type
        self.line = line
        self.list = []
        self.father = ""
        self.flag = 0

    def add(self, value):
        self.list.append(value)


class Analysis(QtCore.QObject):
    stop_signal = QtCore.pyqtSignal(str)

    def __init__(self, filename, config_ini, parent=None):
        super(Analysis, self).__init__(parent)
        self.master = parent
        self.filename = filename
        self.filelist = []
        self.vallist = []
        self.funlist = []
        self.config_ini = config_ini
        self.token_func = []
        self.token_val = []
        self.danger = []
        self.invalid_func = []
        self.invalid_val = []

        self.validfun = []
        self.validval = []

    def run(self):
        self.get_function()
        self.gen_token()
        self.gen_danger()
        self.gen_invalid()
        return self.token_func, self.token_val, self.danger, self.invalid_func, self.invalid_val

    def get_function(self):
        path, name = os.path.split(self.filename)
        self.get_file(path)
        cpath = self.config_ini['main_project']['project_path'] + self.config_ini['scanner']['ctags']
        cmd = cpath + " --languages=c -R -I argv --kinds-c=+defglmpstuvx --fields=+n"
        for file in self.filelist:
            cmd += " " + file
        os.system(cmd)
        f = open("tags", "r")
        code = f.readlines()
        f.close()

        for line in code:
            if line.startswith("!_TAG"):
                continue
            split_line = line.split('\t')
            func = Function(name=split_line[0], filepath=split_line[1])
            if len(split_line) == 8 or len(split_line) == 6:
                func.line = split_line[4]
                func.type = split_line[3]

                if func.type == 'l':
                    func.val_type = split_line[6].split(":")[-1]
                    func.father = split_line[5].split(":")[-1]
                    self.vallist.append(func)
                else:
                    func.val_type = split_line[5].strip("\n").split(":")[-1]
                    if func.type == 'f':
                        self.funlist.append(func)
                    else:
                        if func.type == 's':
                            func.val_type = "struct"
                        self.vallist.append(func)
            elif len(split_line) == 9:
                func.line = split_line[5]
                func.type = split_line[4]
                if func.type == 'm':
                    func.val_type = split_line[7].split(":")[-1]
                    func.father = split_line[6]
                    self.vallist.append(func)
                if func.type == 'l':
                    func.val_type = split_line[7].split(":")[-2]+" "+split_line[7].split(":")[-1]# TODO:可优化，代改
                    func.father = split_line[6].split(":")[-1]
                    self.vallist.append(func)
        for i in self.vallist:
            if i.type == 'm':
                for v in self.vallist:
                    if v.type == 's':
                        self.vallist[self.vallist.index(v)].add(i)
            elif i.type == 'l':
                for f in self.funlist:
                    if i.filepath == f.filepath and i.father == f.name:
                        self.funlist[self.funlist.index(f)].add(i)

    def get_file(self, path):
        list = []
        files = os.listdir(path)
        for file in files:
            if re.match("(\w*)\.c", file) is not None:
                f = path + '/' + file
                if not os.path.isdir(f):
                    list.append(f)
        self.filelist = list

    def gen_token(self):
        c_parser = CParser(self.filename)
        print(self.filename)
        parameters = c_parser.get_parameters()

        # for fun1 in self.funlist:
        #     for fun2 in self.funlist:
        #         if fun1 != fun2 and fun1.name == fun2.name:
        #             self.funlist.remove(fun2)


        for fun in self.funlist:
            print(":::::::::::", fun.name, fun.list, fun.line)

        for func in self.funlist:
            f = [func.filepath, func.name, func.line, func.val_type, []]
            if func.list:
                for val in func.list:
                    ll = [val.name, val.line, val.val_type]
                    f[-1].append(ll)
            for param in parameters:
                print(func.name, "asdasdasdasdasdasdasdasdasdasdad", param[0], len(param))
                print(param)
                if func.name == param[0] and len(param) > 1:
                    print("......................", param[0], "........................")
                    for i in range(1,len(param)):
                        ff = [param[i][0], "line:" + str(param[i][1]), param[i][2]]
                        f[-1].append(ff)
                        print(ff)

            self.token_func.append(f)

        for val in self.vallist:
            if val.type != 's' and val.type != 'v':
                continue
            v = [val.filepath, val.name, val.line, val.val_type, []]
            if val.list:
                for i in val.list:
                    ii = [i.name, i.line, i.val_type]
                    v[-1].append(ii)
            self.token_val.append(v)



    def gen_danger(self):
        for file in self.filelist:
            dangers=Danger(file, self.config_ini)
            dangers.findDanger()
            self.danger.extend(dangers.danger)
        of = overflowAnalyzer(self.filename)
        dangerList = of.outputDanger()
        for danger in dangerList:
            self.danger.extend(danger)

    def gen_invalid(self):
        for f in self.funlist:
            if f.name =='main':
                main = f
                # break
        self.validfun.append(main)
        self.find_valid(main, [])
        for f in list(set(self.funlist) - set(self.validfun)):
            ff = [f.filepath, f.line, f.name]
            self.invalid_func.append(ff)

        for v in list(set(self.vallist) - set(self.validval)):
            vv = [v.filepath, v.line, v.name]
            self.invalid_val.append(vv)

    def find_valid(self, fun, l):
        code = self.scanner(fun.filepath)
        print(code)
        flag = 0
        first = True
        l.append(fun)
        fline = fun.line.split(":")[-1]
        for line in code[int(fline):]:
            if len(line) > 1:
                if line[1] == '{' or line[-1] == '{':
                    flag += 1
                    first = False
                if line[1] == '}' or line[-1] == '}':
                    flag -= 1
            if flag == 0 and first == False:
                break
            for v in self.vallist:
                if v.name in line:
                    index = line.index(v.name)
                    if len(line) > index + 1:
                        if line[index + 1] != "(" and v.line != "line:" + self.get_linenum(line[0]) and v in fun.list:
                            self.validval.append(v)
                    else:
                        if v.line != "line:" + self.get_linenum(line[0]) and v in fun.list:
                            self.validval.append(v)
            for v in self.vallist:
                if v.name in line and v not in self.validval and v.filepath == fun.filepath:
                    index = line.index(v.name)
                    if len(line) > index + 1:
                        if line[index + 1] != "(" and v.line != "line:" + self.get_linenum(line[0]):
                            print(line)
                            self.validval.append(v)
                    else:
                        if v.line != "line:" + self.get_linenum(line[0]):
                            self.validval.append(v)
            for f in self.funlist:
                if f.name in line and f not in self.validfun:
                    index = line.index(f.name)
                    if line[index + 1] == '(' and f.line != "line:" + self.get_linenum(line[0]):
                        self.validfun.append(f)
        if self.validfun != l:
            for f in list(set(self.validfun) - set(l)):
                self.find_valid(f, l)

    def scanner(self, fileName):
        path = self.config_ini['main_project']['project_path'] + self.config_ini['result']['demo']
        f = open(path, "w")
        text = "0$" + fileName + "$\n"
        f.write(text)
        f.close()
        cmd = self.config_ini['main_project']['project_path'] + self.config_ini['scanner']['lex'] + " < " + fileName
        os.system(cmd)
        f = open(path, "r")
        list = f.readlines()
        code = []
        for s in list:
            s.rstrip()
            str = s.split("$")
            result = [x.strip() for x in str if x.strip() != '']
            code.append(result)
        print(code)
        return code

    def get_linenum(self, line):
        pattern = re.compile("[0-9]+")
        m = re.search(pattern, line)
        return m.group(0)
