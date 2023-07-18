from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet
from startWin import MainWindow
from Login import logWin
from ui.loadWidget import LoadingDialog

if __name__ == '__main__':

    app = QApplication([])
    app.setWindowIcon(QIcon("ui/resource/img/Audit.png"))
    # window = MainWindow() # 关
    window = logWin() # 开
    # window = LoadingDialog()
    # apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True,css_file='ui/light_style.css')
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True, css_file='ui/light_style.css')
    window.show()
    app.exec_()
