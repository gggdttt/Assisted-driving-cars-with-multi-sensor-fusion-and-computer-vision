from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
import time
import sys


class BackendThread(QObject):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit(str(currTime))
            time.sleep(1)


class Window(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('PyQt 5界面实时更新例子')
        self.resize(400, 100)
        self.input = QLineEdit(self)
        self.input.resize(400, 100)
        self.initUI()

    def initUI(self):
        # 创建线程
        self.backend = BackendThread()
        # 连接信号
        self.backend.update_date.connect(self.handleDisplay)
        self.thread = QThread()
        self.backend.moveToThread(self.thread)
        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    # 将当前时间输出到文本框
    def handleDisplay(self, data):
        self.input.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())