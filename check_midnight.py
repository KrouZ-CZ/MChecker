import os
from PyQt5 import QtCore

class check_midnight(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(list)
    fineshed = QtCore.pyqtSignal()

    def __init__(self, path, parent=None) -> None:
        QtCore.QThread.__init__(self, parent)
        self.path = path

    def run(self):
        self.mysignal.emit(['START', self.path])
        self.next_dir = []
        self.files_path = []
        self.exe_files = []
        self.errors = []
        self.files_path = self.start(self.path)
        self.a = 0
        self.sort()
        self.result()

    def start(self, path):
        filenames = []
        self.mysignal.emit(['CHECK', path])
        for i in os.listdir(path):
            if os.path.isdir(os.path.join(path, i)):
                try: filenames += self.start(os.path.join(path, i))
                except Exception as e: self.errors.append(e)
            else:
                filenames.append(os.path.join(path, i))
        return filenames

    def sort(self):
        for i in self.files_path:
            if os.path.basename(i).split('.')[-1].lower() == 'exe':
                self.exe_files.append(i)

    def result(self):
        self.mysignal.emit(['CHECK', 'Вывожу результаты'])
        for i in self.errors:
            self.mysignal.emit(['ERRORS', i])
        for i in self.files_path:
            try:
                if int(os.path.getsize(i)) > 10000000 and int(os.path.getsize(i)) < 12000000:
                    self.mysignal.emit(['SOSO', i])
                    self.a += 1
            except:
                pass
        for i in self.exe_files:
            try:
                file_dat = os.path.join(os.path.dirname(i), ''.join(os.path.basename(i).split('.')[0:-1])) + '.dat'
                if os.path.exists(file_dat):
                    self.mysignal.emit(['OK', i])
                    self.a += 1
                if int(os.path.getsize(i)) > 10000000 and int(os.path.getsize(i)) < 12000000:
                    self.mysignal.emit(['OK', i])
                    self.a += 1
            except:
                pass
        if self.a == 0:
            self.mysignal.emit(['NONE'])
        else:
            pass
        self.mysignal.emit(['EXIT'])
        self.fineshed.emit()