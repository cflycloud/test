from PyQt5.Qsci import QsciScintilla
from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QColor, QSyntaxHighlighter
import PyQt5.QtWidgets
from .myCustomLexer import CustomLexer
from ui.findWidget import Ui_findDialog
import re


class FindForm(QDialog, Ui_findDialog):
    def __init__(self, parent = None):
        super(FindForm, self).__init__(parent)
        self.setupUi(self)
        self.master = parent
        self.pushButton.clicked.connect(self.find_btn)
        self.pushButton_3.clicked.connect(self.replace_btn)
        self.pushButton_4.clicked.connect(self.replaceall_btn)
        # 保存原来的lexer
        self.previousLexer = self.master.tabWidget.currentWidget().lexer()
        self.prompt = ['XXXXX']
        self.searchNum = 0

    def find_btn(self):
        self.label.clear()
        text = self.lineEdit.text()

        if self.prompt[-1] != text:
            flag = 1
            if self.prompt[-1] == 'XXXXX':
                flag = 0
            self.prompt.append(text)
        else:
            flag = 0

        textEdit = self.master.tabWidget.currentWidget()

        if flag:
            textEdit.setLexer(self.previousLexer)

        # 使用正则表达式搜索
        if self.checkBox.isChecked():
            matches = list(re.finditer(text, textEdit.text()))
            matched_strings = [match.group() for match in matches]
            count = len(matches)
            founded = bool(matches)
            print(matched_strings)
            if matches:
                textEdit.findFirst(matched_strings[self.searchNum % len(matched_strings)], False, True, True, True)
                print("searchNum: ", self.searchNum)
                self.searchNum += 1
                for match in matches:
                    matched_text = match.group()
                    textEdit.highlight_string(matched_text)
            if not founded:
                textEdit.setCursorPosition(0, 0)
                self.searchNum = 0
                matches = list(re.finditer(text, textEdit.text()))
                textEdit.findFirst(matched_strings[0], False, True, True, True)
                founded = bool(matches)

        else:
            # 高亮搜索字符串
            count = textEdit.highlight_string(text)
            founded = textEdit.findFirst(text, False, True, True, True)
            if not founded:
                textEdit.setCursorPosition(0, 0)
                founded = textEdit.findFirst(text, False, True, True, True)

        print("count:", count)
        print("founded:", founded)

        if count:
            self.label.setStyleSheet("QLabel {color: green;}")
            self.label.setText(
                "找到 \"{}\" {} 次".format(
                    self.lineEdit.text(),
                    count
                )
            )

        if not founded and not count:
            # 如果仍然没有找到，那么显示没有找到的信息
            self.label.setStyleSheet("QLabel {color: red;}")
            self.label.setText(
                "没有找到 \"{}\"".format(
                    self.lineEdit.text()
                )
            )

    def replace_btn(self):
        self.label.setText('')
        self.master.tabWidget.currentWidget().replace(self.lineEdit_2.text())

    def replaceall_btn(self):
        self.label.setText('')
        textEdit = self.master.tabWidget.currentWidget()
        replaced = 0
        text = self.lineEdit.text()
        founded = textEdit.findFirst(text, self.checkBox.isChecked(), True, True, True)
        while founded:
            textEdit.replace(self.lineEdit_2.text())
            founded = textEdit.findNext()
            replaced += 1

        self.label.setStyleSheet("QLabel {color: red;}")
        self.label.setText(f"{replaced}处被替换")

    # 重写closeEvent方法
    def closeEvent(self, event):
        # 在关闭窗口时恢复原来的lexer
        textEdit = self.master.tabWidget.currentWidget()
        textEdit.setLexer(self.previousLexer)
        event.accept()
