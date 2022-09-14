import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from des import *
from check_midnight import check_midnight

class App(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.folder)
        self.ui.pushButton_2.clicked.connect(self.start)
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.textEdit.setText(''))
    
    def folder(self):
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.ui.lineEdit.setText(self.folderpath)

    def start(self):
        if self.ui.lineEdit.text() == '': return
        self.thread = QtCore.QThread()
        self.signal = check_midnight(self.ui.lineEdit.text())
        self.signal.moveToThread(self.thread)
        self.signal.mysignal.connect(self.signal_handler)
        self.thread.started.connect(self.signal.run)
        self.signal.fineshed.connect(self.thread.quit)
        self.signal.fineshed.connect(self.signal.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.ui.pushButton_2.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.ui.pushButton_2.setEnabled(True)
        )
        self.thread.start()

    def signal_handler(self, signal):
        if signal[0] == 'START':
            self.ui.textEdit.append(f'Начинаю сканирование: {signal[1]}')
        elif signal[0] == 'CHECK':
            self.ui.label_2.setText(f'Идёт проверка: {signal[1]}')
        elif signal[0] == 'ERRORS':
            self.ui.textEdit.append(str(signal[1]))
        elif signal[0] == 'SOSO':
            self.ui.textEdit.append(f'[/] - {signal[1]} -')
        elif signal[0] == 'OK':
            self.ui.textEdit.append(f'[!] - {signal[1]} -')
        elif signal[0] == 'NONE':
            self.ui.textEdit.append('[+] MIDNIGHT Не обнаружен')
        elif signal[0] == 'EXIT':
            self.ui.label_2.setText('Идёт проверка: None')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())